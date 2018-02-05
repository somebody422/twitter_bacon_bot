from twython import Twython
import json
import sys
import re

import const
from state_machine import KevinBaconStateMachine

import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

# enter your keys, and tokens obtained from your twitter app


"""
twitter = Twython(
	app_key = consumer_key, 
	app_secret = consumer_secret,
	oauth_token = access_token,
	oauth_token_secret = access_token_secret
)
"""

def pretty(d, indent=0):
	for key, value in d.items():
		print('  ' * indent + str(key))
		if isinstance(value, dict):
			pretty(value, indent+1)
		else:
			s = '  ' * (indent+1) + unicode(value)
			print(s.encode('ascii', 'ignore'))


def add_newlines_to_json(json_str):
	return re.sub(r'([,}])', r'\1\n', json_str)

def print_search_response(response):
	print("Search returned %d results with query \"%s\"" % 
		(response['search_metadata']['count'],
		 response['search_metadata']['query'])
	)
	print("Statuses: %d" % len(response['statuses']))
	for status in response['statuses']:
		print("Tweet id: %s" % status['id'])
		print("  User: %s" % status['user']['name'])
		print("  url: %s" % status['entities']['urls'][0][u'url'])
		print("  text: \"%s\"" % status['text'])
		print("  mentions:")
		for mention in status['entities']['user_mentions']:
			print("    %s" % mention)
		print('\n')



def main():
	#query = "from:%s" % sys.argv[1]
	#query = str(sys.argv[1])
	#response = twitter.search(q = query, count = 3)

	"""
	for item in x['statuses']:
		if type(x) == dict:
			pretty(item)
		else:
			print(item)
	"""

	#print(x)
	#print("got %d tweets!" % response['search_metadata']['count'])
	#print(len(response['statuses']))
	#pretty(response['statuses'][0])

	#print_search_response(response)

	if len(sys.argv) != 2:
		print("Usage: python kb.py START_USERNAME")
		sys.exit(1)
	name = str(sys.argv[1])
	state_machine = KevinBaconStateMachine()
	state_machine.run(name)


if __name__ == '__main__': 
	main()

