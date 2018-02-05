"""
meant to be run with "python -i twython" so I
 don't have to copy paste those keys to do some
 interactive stuff
"""


import twython
import pprint

t = twython.Twython(
	"XyIlOeuwm7Rswl9fGy5j5P0nH",
	"tX9N8vRf4m9t1ogFRXhomt34lGIs4EEGY8VfH5rb4apREVqiAj",
	"959179660037935104-c6Bl7XEKycJFUWdj3GBaa79x4jbpyN2",
	"MpYDQLjxUGyc7w0BL8l8K7sZNkfWJ3HALbid48GO8jlTB"
)

p = pprint.PrettyPrinter(indent=2)