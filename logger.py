"""
A class to provide logging capabilities.

Follows a simple singleton pattern. Not reaaly robust
 because it doesn't need to be
"""

import os
import time
import random

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
	@staticmethod
	def init(level, username):
		# Filename is the start username, current unix time, and some
		#  extra random numbers if we need that for some reason
		path = 'logs' + os.sep + username + '_' + str(int(time.time()))
		while os.path.exists(path + '.log'):
			path = path + random.randint(0,9)
		path = path + '.log'
		Logger._instance = Logger(level, path)


	# Close the file and do any necessary cleanup
	@staticmethod
	def done():
		Logger._instance.close()


	######### Instance stuff ###########

	def __init__(self, loglevel, path):
		print("making logger object with path: %s" % path)
		self.path = path
		self.loglevel = loglevel
		self.file = open(path, 'w')
		self.file.write(time.strftime("Log started: %m/%d/%y %H:%m %Ss\n", time.gmtime()))

	def close(self):
		self.file.close()

	# 0: Print and log nothing
	# 1: Print nothing, log everything
	# 2: Print everthing, log everything
	def log(self, s):
		if self.loglevel == 1:
			self.file.write(s)
			self.file.write('\n')
		elif self.loglevel == 2:
			self.file.write(s)
			self.file.write('\n')
			print(s)

	# maybe logs the string, but is guarenteed to print the
	#  string
	def logAndForcePrint(self, s):
		if self.loglevel == 1 or self.loglevel == 2:
			self.file.write(s)
			self.file.write('\n')
		print(s)
