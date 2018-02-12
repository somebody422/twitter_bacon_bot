from twython import Twython
import json
import sys

from state_machine import KevinBaconStateMachine

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


def main():
	if len(sys.argv) != 2:
		print("Usage: python kb.py START_USERNAME")
		sys.exit(1)
	name = str(sys.argv[1])
	state_machine = KevinBaconStateMachine(name)
	state_machine.run()



if __name__ == '__main__': 
	main()

