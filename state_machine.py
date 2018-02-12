"""
A simple implementation of a state machine. An implementation should extend
this class and add states/transitions in constructor

Essentially is just a graph
"""


"""
BFS
next_nodes = list of working nodes. pop off from the front
previous = dictionary mapping node name to previous node name

"""


import const
import time
import twython
import re
from sys import stdout
from collections import deque


# Class which will be inherited by our state machine
class StateMachine(object):
	def __init__(self):
		self.states = {}
		self.transitions = {}
		self.addState('start', self.startState)
		self.current_state = "start"
		self.next_state = ""
		

	def addState(self, state_name, f):
		self.states[state_name] = f


	def addTransition(self, from_state, to_state, f):
		# Transition name is from_state and to_state names concatenated
		self.transitions[from_state+to_state] = f


	def run(self):
		while True:
			# Run the current state until someone sets the next one
			while self.next_state == "":
				self.states[self.current_state]()

			if self.next_state == 'end':
				break

			# self.next_state has been set, time to go to it. First try
			#  to run a transition funciton if we have one
			transition_name = self.current_state+self.next_state
			if transition_name in self.transitions:
				self.transitions[transition_name]()

			# Finally, set the next state and 
			self.current_state = self.next_state
			self.next_state = ""

		# Broke out of loop, done running state machine
		print("Exiting state machine")


	def startState(self):
		print("If you're seeing this text, the state machine was not initialized correctly! Make sure to set next_state in the constructor")


"""
States:
not_connected - Unable to connect to twitter, or internet
searching - Connected to twitter, searching through tweets
data_capped - Reached data cap. Periodically tries to make requests
success - Found a path to kevin bacon
fail - Out of nodes, unable to find a path
"""
class KevinBaconStateMachine(StateMachine):
	def __init__(self, start_node):
		super(KevinBaconStateMachine, self).__init__()
		self.connected = False
		self.working_nodes = deque()
		self.previous = {}
		self.num_iterations = 0
		self.start_node = start_node
		self.working_nodes.append(start_node)
		self.addState('not_connected', self.notConnectedState)
		self.addState('searching', self.searchingState)
		self.addState('data_capped', self.dataCappedState)
		self.addState('success', self.successState)
		self.addState('fail', self.failState)
		self.addTransition('start', 'searching', self.tryToConnect)
		self.addTransition('not_connected', 'searching', self.tryToConnect)
		self.next_state = 'searching'


	def tryToConnect(self):
		if self.connected == True:
			return

		self.twitter = twython.Twython(
			app_key = const.consumer_key, 
			app_secret = const.consumer_secret,
			oauth_token = const.access_token,
			oauth_token_secret = const.access_token_secret
		)

		# Test if we are actually connected
		number_of_connect_attempts = 0
		connected = False
		while(not connected):
			try:
				# This actually gets a JSON response. However, we just
				#  want to know if if fails (throws an exception).
				print("verifying credentials..")
				self.twitter.verify_credentials()
				connected = True
				next_state = 'searching'
			except twython.exceptions.TwythonAuthError:
				if number_of_connect_attempts >= const.max_connection_attempts:
					print("Unable to authenticate correctly!")
					self.next_state = 'not_connected'
					return
				print("Unable to authenticate correctly! retrying..")
				number_of_connect_attempts += 1
				time.sleep(2)
			except twython.exceptions.TwythonRateLimitError:
				print("Hit rate limit")
				self.next_state = 'data_capped'
				return


	def notConnectedState(self):
		print("type \'connect\' to try again, or \'exit\' to end program")
		s = raw_input()
		if s == "connect":
			self.next_state = 'searching'
		elif s == "exit":
			self.next_state = 'end'


	def searchingState(self):
		if len(self.working_nodes) < 1:
			self.next_state = 'fail'
			return

		node = self.working_nodes.popleft()
		try:
			result = self.twitter.search(
				q = "from:" + node,
				result_type = 'recent',
				count = 100,
				tweet_mode = 'extended'
			)
		except twython.exceptions.TwythonAuthError:
			print("Error conecting to twitter")
			self.next_state = 'not_connected'
			return
		except twython.exceptions.TwythonRateLimitError:
			print("Hit rate limit")
			self.next_state = 'data_capped'
			return

		print('\n')
		print("Looking at \'" + node + "\'")
		print(str(len(result['statuses'])) + ' tweets')
		for status in result['statuses']:
			print('\n')
			if re.search(r'@kevinbacon|kevin bacon|kevin_bacon', status['full_text'], flags=re.IGNORECASE):
				# Found a path to kevin bacon!!
				self.success_node = node
				self.success_status = status
				self.next_state = 'success'
				return
			print(status['full_text'])
			for mentioned_user in status['entities']['user_mentions']:
				mentioned_user_name = mentioned_user['screen_name']
				if mentioned_user_name != node and mentioned_user_name not in self.previous:
					# Add the node to the working_nodes list
					#print("Adding to queue: " + mentioned_user_name)
					self.previous[mentioned_user_name] = node
					self.working_nodes.append(mentioned_user_name)


		if const.max_iterations != -1:
			if self.num_iterations >= const.max_iterations:
				self.next_state = 'fail'
			else:
				self.num_iterations += 1



	def dataCappedState(self):
		print("waiting")
		time.sleep(const.secs_between_tries_while_data_capped)
		try:
			self.twitter.verify_credentials()
			# Success!
			next_state = 'searching'
		except twython.exceptions.TwythonAuthError:
			print("Error conecting to twitter")
			self.connected = False
			self.next_state = 'not_connected'
		except twython.exceptions.TwythonRateLimitError:
			print("Waiting for data cap to end..")
		except:
			print("exception")



	def successState(self):
		print("Success!")
		
		# print out path
		path = ['kevinbacon', self.success_node]
		temp_node = self.success_node
		while temp_node != self.start_node:
			temp_node = self.previous[temp_node]
			path.append(temp_node)

		for node in reversed(path):
			stdout.write(" -> " + node)
		print('\n')

		print("Tweet text:")
		print(self.success_status['full_text'])
		print('\n')

		# for debugging, print out status of state machine..
		print(self.working_nodes)
		print('\n')
		print(self.previous)

		self.next_state = 'end'


	"""
	Should never really go here ideally. I used this while debugging, and will leave it in for now.
	"""
	def failState(self):
		print("failure :(")
		self.next_state = 'end'