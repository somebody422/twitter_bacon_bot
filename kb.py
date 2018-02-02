from twython import Twython
import json
import sys
import re

# enter your keys, and tokens obtained from your twitter app
consumer_key = "XyIlOeuwm7Rswl9fGy5j5P0nH"
consumer_secret = "tX9N8vRf4m9t1ogFRXhomt34lGIs4EEGY8VfH5rb4apREVqiAj"
access_token = "959179660037935104-c6Bl7XEKycJFUWdj3GBaa79x4jbpyN2"
access_token_secret = "MpYDQLjxUGyc7w0BL8l8K7sZNkfWJ3HALbid48GO8jlTB"


#twitter =  Twython(consumer_key, consumer_secret,
#                    access_token, access_token_secret)


twitter = Twython(
	app_key = consumer_key, 
	app_secret = consumer_secret,
	oauth_token = access_token,
	oauth_token_secret = access_token_secret
)




def main():
    #query = "from:%s" % sys.argv[1]
    query = str(sys.argv[1])
    x = twitter.search(q=query)
    print x


if __name__ == '__main__': 
    main()