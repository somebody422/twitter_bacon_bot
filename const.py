"""
Constant values, settings
"""

# As this is a GET request, only want to do a few, or risk going over our
#  rate limit
max_connection_attempts = 3
#consumer_key = "x"  # intentially wrong key, to get to not_connected state
consumer_key = "XyIlOeuwm7Rswl9fGy5j5P0nH"
consumer_secret = "tX9N8vRf4m9t1ogFRXhomt34lGIs4EEGY8VfH5rb4apREVqiAj"
access_token = "959179660037935104-c6Bl7XEKycJFUWdj3GBaa79x4jbpyN2"
access_token_secret = "MpYDQLjxUGyc7w0BL8l8K7sZNkfWJ3HALbid48GO8jlTB"
# Number of seconds between attempts to get data, when data
#  capped and waiting
secs_between_tries_while_data_capped = 10

# Should be something very high, or -1 for no max
max_iterations = -1