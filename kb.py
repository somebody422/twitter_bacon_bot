import argparse
from twython import Twython
import json
import sys

from state_machine import KevinBaconStateMachine
from logger import Logger
import const

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

"""
Creates and returns an argparse object
"""
def makeArgParser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--verbosity',
		nargs = '?',
		type = int,
		default = const.default_verbosity_level,
		help = "Level of printing/logging, see const.py for more info"
	)
	parser.add_argument('username',
		nargs = 1,
		help = "The username to start the search from"
	)
	return parser

def main():

	"""
	if len(sys.argv) != 2:
		print("Usage: python kb.py START_USERNAME")
		sys.exit(1)
	name = str(sys.argv[1])
	state_machine = KevinBaconStateMachine(name)
	state_machine.run()
	"""
	parser = makeArgParser()
	args = parser.parse_args()
	print(args)
	print(args.username)

	logger.init()



if __name__ == '__main__': 
	main()

