#
# Chordially - Utilities.py
# Bits and bobs for the Chordially project
#
# Jonatan H Sundqvist
# December 14 2014
#

# TODO | -
#        -
#
# SPEC | -
#        -




DEBUG = False

if not DEBUG:
	def debug(*args, **kwargs):
		pass
else:
	def debug(*args, **kwargs):
		# Dangerous hack
		caller = getframeinfo(currentframe().f_back)
		print('[{0.lineno}]'.format(caller), end=' ')
		print(*args, **kwargs)



def main():

	'''
	Test suite

	'''

	pass



if __name__ == '__main__':
	main()