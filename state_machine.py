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


import time
import twython
import re
from sys import stdout
from collections import deque

import const
from logger import Logger


# Class which will be inherited by our state machine
class StateMachine(object):
	def __init__(self):
		self.states = {}
		self.transitions = {}
		self.addState('start', self.startState)
		self.addState('end', self.endState)
		self.current_state = "start"
		self.next_state = ""
		

	def addState(self, state_name, f):
		self.states[state_name] = f


	def addTransition(self, from_state, to_state, f):
		# Transition name is from_state and to_state names concatenated
		self.transitions[from_state+to_state] = f


	def run(self):
			while True:
				# This usually will run until I do a ctl-c. I would prefer that it
				#  ends gracefully and prints out some info
				try:
					# Run the current state until someone sets the next one
					while self.next_state == "":
						self.states[self.current_state]()

					if self.next_state == 'quit':
						break

					# self.next_state has been set, time to go to it. First try
					#  to run a transition funciton if we have one
					transition_name = self.current_state+self.next_state
					if transition_name in self.transitions:
						self.transitions[transition_name]()

					# Finally, set the next state
					self.current_state = self.next_state
					self.next_state = ""

				except KeyboardInterrupt:
					self.next_state = 'end'
					continue


	def startState(self):
		print("If you're seeing this text, the state machine was not initialized correctly! Make sure to set next_state in the constructor")

	# If a child class wants to do some cleanup or whatever, it can
	#  happen in the edge to this state
	def endState(self):
		print("Exiting state machine")
		self.next_state = 'quit'


"""
States:
not_connected - Unable to connect to twitter, or internet, data capped
searching - Connected to twitter, searching through tweets

vv getting rid of this vv
data_capped - Reached data cap. Periodically tries to make requests
^^^^^^^^^^^^^^^^^^^^^^^^^^

A few notes on the searching algorithm and twitter API:
 * API will not return old tweets like the browser search does. Have
    not been able to find a way around this :(
"""
class KevinBaconStateMachine(StateMachine):
	def __init__(self, start_node):
		super(KevinBaconStateMachine, self).__init__()
		#self.connected = False
		self.working_nodes = deque()
		self.previous = {}
		self.num_iterations = 0
		self.start_node = start_node
		self.working_nodes.append(start_node)
		# true when we find a path to kb himself
		self.success = False
		self.addState('not_connected', self.notConnectedState)
		self.addState('searching', self.searchingState)
		#self.addState('data_capped', self.dataCappedState)
		#self.addState('success', self.successState)
		#self.addState('fail', self.failState)
		self.addTransition('start', 'not_connected', self.startKBStateMachine)
		#self.addTransition('not_connected', 'searching', self.tryToConnect)
		self.addTransition('not_connected', 'end', self.shutdownKBStateMachine)
		#self.addTransition('data_capped', 'end', self.shutdownKBStateMachine)
		self.addTransition('searching', 'end', self.shutdownKBStateMachine)
		self.next_state = 'not_connected'
		self.logger = Logger.instance()

		self.twitter = twython.Twython(
			app_key = const.consumer_key, 
			app_secret = const.consumer_secret,
			oauth_token = const.access_token,
			oauth_token_secret = const.access_token_secret
		)

	"""
	First thing to run, before we try to initially connect
	"""
	def startKBStateMachine(self):
		self.start_time = time.time()

	"""
	Tries a few times to get a successful response from twitter.
	 Returns true if connected
	"""
	def tryToConnect(self):
		#if self.connected == True:
		#	return

		#self.twitter = twython.Twython(
		#	app_key = const.consumer_key, 
		#	app_secret = const.consumer_secret,
		#	oauth_token = const.access_token,
		#	oauth_token_secret = const.access_token_secret
		#)

		number_of_connect_attempts = 0
		#connected = False
		while(number_of_connect_attempts < const.max_connection_attempts):
			try:
				# This actually gets a JSON response. However, we just
				#  want to know if if fails (throws an exception).
				#self.logger.log("verifying credentials..")
				self.twitter.verify_credentials()
				#connected = True
				#next_state = 'searching'
				return True
			# Our authentication is bad, or it changed
			except twython.exceptions.TwythonAuthError:
				#if number_of_connect_attempts >= const.max_connection_attempts:
				#	self.logger.logAndForcePrint("Going to not_connected state")
				#	self.next_state = 'not_connected'
				#	return
				number_of_connect_attempts += 1
				#time.sleep(2)
			# Twitter is blocking us out
			except twython.exceptions.TwythonRateLimitError:
				#self.logger.logAndForcePrint("Going to data_capped state")
				#self.next_state = 'data_capped'
				return False
			# Twython tried and failed. possibly due to a broken 
			#  internet connection
			except twython.exceptions.TwythonError:
				return False
			time.sleep(2)


	def notConnectedState(self):
		"""
		print("type \'connect\' to try again, or \'exit\' to end program")
		s = raw_input()
		if s == "connect":
			self.next_state = 'searching'
		elif s == "exit":
			self.next_state = 'end'
		"""
		#logger.log("Trying to connect..")
		got_connection = self.tryToConnect()
		if got_connection:
			self.logger.logAndForcePrint("Going to searching state")
			self.next_state = 'searching'
			#self.connected = True
			return
		time.sleep(const.secs_between_tries_while_data_capped)

	def dataCappedState(self):
		time.sleep(const.secs_between_tries_while_data_capped)
		try:
			self.twitter.verify_credentials()
			# Success!
			self.logger.logAndForcePrint("Going to searching state")
			next_state = 'searching'
		except twython.exceptions.TwythonAuthError:
			self.logger.logAndForcePrint("Going to not_connected state")
			self.connected = False
			self.next_state = 'not_connected'
		#except twython.exceptions.TwythonRateLimitError:
			#print("Waiting for data cap to end..")


	def searchingState(self):
		if len(self.working_nodes) < 1:
			self.logger.logAndForcePrint("Out of nodes to try")
			self.logger.logAndForcePrint("Going to end state")
			self.next_state = 'end'
			return

		node = self.working_nodes.popleft()
		try:
			result = self.twitter.search(
				q = "from:" + node,
				result_type = 'recent',
				# 100 is the max allowed by the API
				count = 100,
				tweet_mode = 'extended'
			)
		except twython.exceptions.TwythonAuthError:
			self.logger.logAndForcePrint("Error conecting to twitter")
			self.next_state = 'not_connected'
			return
		except twython.exceptions.TwythonRateLimitError:
			self.logger.logAndForcePrint("Hit rate limit")
			self.next_state = 'data_capped'
			return

		self.logger.log('\n')
		self.logger.log("Looking at \'" + node + "\'")
		self.logger.log(str(len(result['statuses'])) + ' tweets')
		for status in result['statuses']:
			if re.search(r'@kevinbacon|kevin bacon|kevin_bacon', status['full_text'], flags=re.IGNORECASE):
				# Found a path to kevin bacon!!
				self.success_node = node
				self.success_status = status
				self.success = True
				self.next_state = 'end'
				self.logger.logAndForcePrint("Going to end state")
				return
			for mentioned_user in status['entities']['user_mentions']:
				mentioned_user_name = mentioned_user['screen_name']
				if mentioned_user_name != node and mentioned_user_name not in self.previous:
					# Add the node to the working_nodes list
					#print("Adding to queue: " + mentioned_user_name)
					self.previous[mentioned_user_name] = node
					self.working_nodes.append(mentioned_user_name)


		if const.max_iterations != -1:
			if self.num_iterations >= const.max_iterations:
				self.next_state = 'end'
			else:
				self.num_iterations += 1



	# State machine is going to the 'end' state
	def shutdownKBStateMachine(self):
		# Mark!
		end_time = time.time()

		# If successful, print out the path and tweet
		if self.success:
			self.logger.logAndForcePrint("Success!")
			path = ['kevinbacon', self.success_node]
			temp_node = self.success_node
			while temp_node != self.start_node:
				temp_node = self.previous[temp_node]
				path.append(temp_node)

			for node in reversed(path):
				stdout.write(" -> " + node)
			self.logger.logAndForcePrint('\n')
			self.logger.logAndForcePrint("Tweet text:")
			self.logger.logAndForcePrint(self.success_status['full_text'])
			self.logger.logAndForcePrintprint('\n')

		# Otherwise, complain about this project being too hard
		else:
			self.logger.logAndForcePrint("Unable to find a path to kevin bacon")
		
		# Print out some info about this run
		running_time = end_time - self.start_time
		minutes, seconds = divmod(running_time, 60)
		hours, minutes = divmod(minutes, 60)
		self.logger.logAndForcePrint("Ran for %d hours, %d minutes, and %d seconds" % (hours, minutes, seconds) )

		Logger.done()



"""
	def successState(self):
		
		
		# print out path
		path = ['kevinbacon', self.success_node]
		temp_node = self.success_node
		while temp_node != self.start_node:
			temp_node = self.previous[temp_node]
			path.append(temp_node)

		for node in reversed(path):
			stdout.write(" -> " + node)
		self.logger.logAndForcePrint('\n')

		self.logger.logAndForcePrint("Tweet text:")
		self.logger.logAndForcePrint(self.success_status['full_text'])
		self.logger.logAndForcePrintprint('\n')

		self.next_state = 'end'



	def failState(self):
		self.logger.logAndForcePrint("Exiting state machine")
		Logger.done()
		self.next_state = 'end'
"""