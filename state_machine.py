"""
A simple implementation of a state machine. An implementation should extend
this class and add states/transitions in constructor

Essentially is just a graph
"""

import const
import time
import twython


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
found_result
"""
class KevinBaconStateMachine(StateMachine):
	def __init__(self):
		super(KevinBaconStateMachine, self).__init__()
		self.connected = False
		self.addState('not_connected', self.notConnectedState)
		self.addState('searching', self.searchingState)
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

		# Do a test search to see if we are connected
		number_of_connect_attempts = 0
		connected = False
		while(not connected):
			try:
				# This actually gets a JSON response. However, we just
				#  want to know if if fails (throws an exception).
				self.twitter.verify_credentials()
			except twython.exceptions.TwythonAuthError as ex:
				if number_of_connect_attempts >= const.max_connection_attempts:
					print("Unable to authenticate correctly!")
					self.next_state = 'not_connected'
					return
				print("Unable to authenticate correctly! retrying..")
				number_of_connect_attempts += 1
				time.sleep(2)
		
		connected = True
		next_state = 'searching'


	def notConnectedState(self):
		print("type \'connect\' to try again, or \'exit\' to end program")
		s = raw_input()
		if s == "connect":
			self.next_state = 'searching'
		elif s == "exit":
			self.next_state = 'end'


	def searchingState(self):
		print("searching state")
		time.sleep(1)