"""
A class to provide logging capabilities.

Follows a simple singleton pattern. Not reaaly robust
 because it doesn't need to be
"""

import os


class Logger:
	########## Static stuff ############
	_instance = None
	
	# Logger.init should be called before Logger.Instance
	#  is ever called!
	@staticmethod
	def instance():
		assert Logger._instance != None
		return Logger._instance

	# Manual init function, should be called in main
	# Creates a unique filename using start user, timestamp,
	#  and some random numbers if necessary
	@staticmethod
	def init(level, username):
		Logger._instance = Logger("name")
		pass


	######### Instance stuff ###########

	def __init__(self, filename):
		self.filename = filename

	def log(self, str):
		print("Logging string: %s" % str)
