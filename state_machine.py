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
"""
class KevinBaconStateMachine(StateMachine):
	def __init__(self, start_node):
		super(KevinBaconStateMachine, self).__init__()
		self.working_nodes = deque()
		self.previous = {}
		self.num_iterations = 0
		self.start_node = start_node
		self.working_nodes.append(start_node)
		# true when we find a path to kb himself
		self.success = False
		self.addState('not_connected', self.notConnectedState)
		self.addState('searching', self.searchingState)
		self.addTransition('start', 'not_connected', self.startKBStateMachine)
		self.addTransition('not_connected', 'end', self.shutdownKBStateMachine)
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
	Constantly trying to re-connect and get back to the searching
	 state
	"""
	def notConnectedState(self):
		got_connection = self.tryToConnect()
		if got_connection:
			self.logger.logAndForcePrint("Going to searching state")
			self.next_state = 'searching'
			return
		time.sleep(const.secs_between_tries_while_not_connected)


	"""
	Tries a few times to get a successful response from twitter.
	 Returns true if connected
	"""
	def tryToConnect(self):
		number_of_connect_attempts = 0
		while(number_of_connect_attempts < const.max_connection_attempts):
			try:
				self.twitter.verify_credentials()
				return True
			# Our authentication is bad, or it changed
			except twython.exceptions.TwythonAuthError:
				number_of_connect_attempts += 1
			# Twitter is blocking us out
			except twython.exceptions.TwythonRateLimitError:
				return False
			# Twython tried and failed. possibly due to a broken 
			#  internet connection
			except twython.exceptions.TwythonError:
				return False
			time.sleep(2)
		return False


	def searchingState(self):
		if len(self.working_nodes) < 1:
			self.logger.logAndForcePrint("Out of nodes to try")
			self.logger.logAndForcePrint("Going to end state")
			self.next_state = 'end'
			return

		node = self.working_nodes.popleft()
		try:
			result = self.twitter.get_user_timeline(
				screen_name = node,
				# 200 is the max allowed
				count = 200,
				tweet_mode = 'extended',
				exclude_replited = True
			)
		except twython.exceptions.TwythonAuthError:
			self.logger.logAndForcePrint("Error conecting to twitter")
			self.logger.logAndForcePrint("Going to not_connected state")
			self.next_state = 'not_connected'
			return
		except twython.exceptions.TwythonRateLimitError:
			self.logger.logAndForcePrint("Hit rate limit")
			self.logger.logAndForcePrint("Going to not_connected state")
			self.next_state = 'not_connected'
			return

		self.logger.log('\n')
		self.logger.log("Looking at \'" + node + "\'")
		self.logger.log(str(len(result)) + ' tweets')
		for status in result:
			if 'retweeted_status' in status:
				# This is the only way I could figure out to determine
				#  if the tweet is a retweet. if it is, then ignore it
				continue
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
					self.previous[mentioned_user_name] = node
					self.working_nodes.append(mentioned_user_name)

		# A max_iterations value of -1 means we keep looping
		#  until the sun implodes
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
			output_string = ""
			for node in reversed(path):
				output_string = output_string + " -> " + node
			self.logger.logAndForcePrint(output_string)
			self.logger.logAndForcePrint('\n')
			self.logger.logAndForcePrint("Tweet text:")
			# If we try to print unicode when python expects ascii, it could
			#  blow up. Convert to utf-8 string here
			success_tweet_text = self.success_status['full_text'].encode('ascii', errors='ignore')
			self.logger.logAndForcePrint(success_tweet_text)
			self.logger.logAndForcePrint('\n')

		# Otherwise, complain about this project being too hard
		else:
			self.logger.logAndForcePrint("Unable to find a path to kevin bacon")
		
		# Print out some info about this run
		running_time = end_time - self.start_time
		minutes, seconds = divmod(running_time, 60)
		hours, minutes = divmod(minutes, 60)
		self.logger.logAndForcePrint("Ran for %d hours, %d minutes, and %d seconds" % (hours, minutes, seconds) )

		Logger.done()
