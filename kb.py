import argparse
from twython import Twython
import json
import sys

from state_machine import KevinBaconStateMachine
from logger import Logger
import const


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


	parser = makeArgParser()
	args = parser.parse_args()

	Logger.init(args.verbosity, args.username[0])
	logger = Logger.instance()
	logger.log("Starting state machine on user %s" % args.username[0])

	state_machine = KevinBaconStateMachine(args.username[0])
	state_machine.run()


if __name__ == '__main__': 
	main()

