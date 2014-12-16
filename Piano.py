#
# Chordially - Piano.py
# Implements a Piano class
#
# Jonatan H Sundqvist
# December 13 2014
#

# TODO | - Keep track of 'dirty' keys to improve rendering performance
#        - API decisions (eg. method arguments or object attributes)
#
# SPEC | -
#        -



from Key import Key
from utilities import debug

import pygame



class Piano(object):

	'''
	Docstring goes here

	'''
	
	def __init__(self, scale=20, compass=(0, 88)):

		'''
		Docstring goes here

		'''

		# Dimensions
		self.dx = 2.0  * scale # Width of a white key
		self.dy = 13.5 * scale # Height of a white key

		self.bdx = 1.2 * scale # Width of a black key
		self.bdy = 8.5 * scale # Height of a black key

		# Settings
		self.keyUtils = Key(0, (self.dx, self.dy), (self.bdx, self.bdy)) 							# Key instance (gives us access to instance methods)
		self.compass  = (self.keyUtils.normalize(compass[0]), self.keyUtils.normalize(compass[1])) 	# Range of keyboard
		debug(self.compass)

		#
		self.surface = pygame.Surface(self.size(padx=10, pady=10, compass=self.compass)) 	# TODO: Fix hard-coded values
		self.keys 	 = self.build(self.compass)												# Create the piano

		# Aesthetics
		self.labelOptions = {'fill': (0x0, 0x0, 0x0)} #
		self.padx = 10
		self.pady = 10

		#
		self.update()

		print('Range is {} to {}.'.format(*compass))
		print('Range is {} to {}.'.format(*self.compass))
		print('Index of {} is {}'.format(compass[0], self.compass[0]))
		print('Index of {} is {}'.format(compass[1], self.compass[1]))


	def width(self, padx=None, dx=None, compass=None):

		'''
		Docstring goes here

		'''

		# NOTE: Many calculations include (compass[1]-compass[1])*7/12,
		# which is an unreliable way of calculating the number of white keys
		return (dx or self.dx) * self.whites(compass) + 2 * (padx or self.padx)


	def height(self, dy=None, pady=0):

		'''
		Docstring goes here

		'''
		
		return (dy or self.dy) + (pady or self.pady) * 2


	def query(self):

		'''
		Docstring goes here

		'''
		# TODO: Rename, merge with Piano.key (?)
		raise NotImplementedError


	def whites(self, compass=None):

		'''
		Total number of white keys in the given range (compass)

		'''

		return sum(1 for i in range(*(compass or self.compass)) if i%12 in Key.whites) # TODO: Find more efficient algorithm (currently O(n))


	def size(self, padx=0, pady=0, dx=None, dy=None, compass=None):
		
		'''
		Size required to fit the entire piano, with optional padding.
		
		Use key word arguments to override self.dx, self.dy and self.compass if you
		so wish.

		'''

		# TODO: Take borders into account (?)
		# TODO: Query methods for keys

		return self.width(dx=dx, padx=padx, compass=compass), self.height(dy=dy, pady=pady)

		
	def render(self, surface, position):

		'''
		Docstring goes here

		'''

		surface.blit(self.surface, position)


	def update(self, keys=True, labels=True, whole=True, accidentals=True):

		'''
		Redraws keys and labels

		'''

		# TODO: Implement options (Enums?)

		for key in self.keys:
			key.render(self.surface, outline=(0,0,0), origin=(self.padx, self.pady), labelled=(key.kind is Key.WHITE), **self.labelOptions)


	def key(self, key):
		# TODO: Use Key alias utilities (...)
		# TODO: Take offset into account (...)
		# TODO: Rename (?)
		# TODO: Make sure this is correct and doesn't break after each change
		debug('Retrieving key {!r} from piano'.format(key))
		debug('Number of keys: ', len(self.keys))
		return self.keys[self.keyUtils.alias(key, to=int)-self.compass[0]]
		# return self.keys[self.keyUtils.alias(key, to=int)]


	def translate(self, dx, dy, vertices):
		return [(vtx[0]+dx, vtx[1]+dy) for vtx in vertices]


	def build(self, compass):

		'''
		Builds the components of the piano

		'''

		# TODO: Options
		# TODO: Animation
		# TODO: Wavefront 3D model
		# TODO: Padding
		# TODO: Individually accessible keys, colour changes
		# TODO: Convert to class (?)
		# TODO: Class for individual keys (press, play, etc.)

		dx,  dy  = self.dx, self.dy
		bdx, bdy = self.bdx, self.bdy

		#   |  |    
		#   |  |    
		#   |  |    
		#  _|  |_   
		# |      |  
		# |      |  
		# |      |  
		# |      |  
		# |______|  

		# return [Key(i, (dx, dy), (bdx, bdy), first=compass[0]) for i in range(*compass)]
		keys = [Key(i, (dx, dy), (bdx, bdy), first=compass[0]) for i in range(*compass)]
		first = keys[5]
		print('Shape:', first.shape)
		print('First: {!r}'.format(first))
		debug('Creating {} keys.'.format(len(keys)))
		debug('Creating {} keys.'.format(self.compass[1]-self.compass[0]))
		if first.shape in (Key.LEFT, Key.MIDDLE):
			# HACK: Solves problem with accidentals as the first key
			first.shape == Key.LEFT
			first.fill = (255, 50, 25)
			first.vertices = first.makeVertices((dx-5, dy-5), (bdx, bdy))

		return keys


	def playChord(self, chord, fill=(210, 190, 50)):
		
		'''
		Docstring goes here
	
		'''

		for note in chord:
			self.key(note).play(fill=fill)
		self.update()


	def releaseChord(self, chord):
		
		'''
		Docstring goes here

		'''

		for note in chord:
			self.key(note).release()
		self.update()


def main():
	
	'''
	Test suite

	'''

	pygame.init()
	piano = Piano()



if __name__ == '__main__':
	main()