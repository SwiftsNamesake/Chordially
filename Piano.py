#
# Chordially - Piano.py
# Implements a Piano class
#
# Jonatan H Sundqvist
# December 13 2014
#

# TODO | - Keep track of 'dirty' keys to improve rendering performance
#        -
#
# SPEC | -
#        -



from Key import Key
from utilities import debug
from SwiftUtils.MultiSwitch import MultiSwitch

import pygame



class Piano(object):

	'''
	Renders an 88-key piano

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
		self.surface = pygame.Surface((self.dx*7*(self.compass[1]-self.compass[0])/12, self.dy)) 	# 
		self.keys 	 = self.build(self.compass)														# Create the piano

		self.update()

		
	def render(self, surface, position):

		'''
		Docstring goes here

		'''

		surface.blit(self.surface, position)


	def update(self):

		'''
		Redraws keys and labels

		'''

		for key in self.keys:
			key.render(self.surface, outline=(0,0,0), origin=(0,0), labelled=(key.kind is Key.WHITE))


	def key(self, key):
		# TODO: Use Key alias utilities
		# TODO: Take offset into account (...)
		return {
			int: 	lambda: self.keys[key-self.compass[0]],					# Index (eg. 5)
			tuple:  lambda: self.keys[(key[1]-1)*7 + 'CDEFGAB'.index(key)], # (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
			str:	lambda: self.keys((key[0], int(key[1]))) 				# Note name (eg. 'G2')
		}[type(key)]()


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

		return [Key(i, (dx, dy), (bdx, bdy), first=compass[0]) for i in range(*compass)]


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