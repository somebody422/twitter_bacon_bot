"""
meant to be run with "python -i twython" so I
 don't have to copy paste those keys to do some
 interactive stuff
"""


import twython
import pprint


p = pprint.PrettyPrinter(indent=2)

def printTimeline(timeline):
	for tweet in timeline:
		try:
			print("user: ")
			print(tweet['user']['name'])
			print("Is a retweet:")
			print('retweeted_status' in tweet)
			print("full_text:")
			print(tweet['full_text'])
			print("\n")
		except UnicodeEncodeError:
			pass

def searchTimelineForString(timeline, s):
	for tweet in timeline:
		try:
			if tweet['full_text'].find(s) != -1:
				print("FOUND IT!!")
				print("retweet:")
				retweeted = 'retweeted_status' in tweet
				print(retweeted)
				#print(tweet['full_text'])
				p.pprint(tweet)
		except UnicodeEncodeError:
			pass


t = twython.Twython(
	"XyIlOeuwm7Rswl9fGy5j5P0nH",
	"tX9N8vRf4m9t1ogFRXhomt34lGIs4EEGY8VfH5rb4apREVqiAj",
	"959179660037935104-c6Bl7XEKycJFUWdj3GBaa79x4jbpyN2",
	"MpYDQLjxUGyc7w0BL8l8K7sZNkfWJ3HALbid48GO8jlTB"
)



# just an example result using timeline
result = t.get_user_timeline(screen_name='david_j_roth', count=20, tweet_mode = 'extended')

