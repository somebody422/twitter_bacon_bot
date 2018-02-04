"""
A simple implementation of a state machine. An implementation should extend
this class and add states/transitions in constructor

Essentially is just a graph
"""

import const
import time


def not_connected()


# Class which will be inherited by our state machine
class StateMachine:

	def __init__(self):
		self.states = {}
		self.transitions = {}
		self.current_state = ""
		self.next_state = ""
		self.twitter = Twython(
			app_key = consumer_key, 
			app_secret = consumer_secret,
			oauth_token = access_token,
			oauth_token_secret = access_token_secret
		)

	def addState(self, state_name, f):
		states[state_name] = f

	def addTransition(self, from_state, to_state, f):
		transitions[from_state+to_state] = f

	def run(self):
		if next_state != "":
			transition_name = current_state+next_state
			if transition_name in transitions:
				transitions[transition_name]()
			current_state = next_state
			next_state = ""
		while next_state == "":
			states[current_state]()


"""
States:
not_connected - Unable to connect to twitter, or internet
searching - Connected to twitter, searching through tweets
"""
class KevinBaconStateMachine(StateMachine):
	def __init__(self):
		super(KevinBaconStateMachine, self).__init__()
		addState('foo', foo)
		current_state = 'foo'

	def foo(self):
		print("in foo!")
		time.sleep(1)
