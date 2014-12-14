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
	
	def __init__(self):

		'''
		Docstring goes here

		'''

		# Dimensions
		self.dx = 2.0  * 20 # Width of a white key
		self.dy = 13.5 * 20 # Height of a white key

		self.bdx = 1.2 * 20 # Width of a black key
		self.bdy = 8.5 * 20 # Height of a black key
		
		# Settings

		#
		self.surface = pygame.Surface((self.dx*88/12*7, 10.0+self.dy)) 	#
		self.keys 	 = self.build()										# Create the piano

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
			key.render(self.surface, outline=(0,0,0), origin=(0,0), labelled=True)


	def key(self, key):
		return {
			int: 	lambda: self.keys[key],									# Index (eg. 5)
			tuple:  lambda: self.keys[(key[1]-1)*7 + 'CDEFGAB'.index(key)], # (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
			str:	lambda: self.keys((key[0], int(key[1]))) 				# Note name (eg. 'G2')
		}[type(key)]()


	def translate(self, dx, dy, vertices):
		return [(vtx[0]+dx, vtx[1]+dy) for vtx in vertices]
		

	def build(self):

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

		# full white, right inset, left inset
		# whiteM = [(0.0, dy), (dx, dy), (dx, bdy), (dx-bdx/2, bdy), (dx-bdx/2, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)] # Middle white
		# whiteL = whiteM[:2] + [(dx, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)] 											# White with left inset
		# whiteR = whiteM[:5] + [(0.0, 0.0), (0.0, dy)] 																		# White with right inset

		# black = self.translate(dx-bdx/2, 0.0, [(0.0, 0.0), (bdx, 0.0), (bdx, bdy), (0.0, bdy)])

		# polygon = pygame.draw.polygon
		# aalines = pygame.draw.aalines

		# # s.fill(colours['BG'])

		# octave = pygame.Surface((dx*7+10, dy+10))

		# for i in range(7):
		# 	self.drawKey(octave, self.translate(dx*i+5.0, 5.0, [whiteR, whiteM, whiteL, whiteR, whiteM, whiteM, whiteL][i])) # Whole note
		# 	self.drawLabel(octave, 'CDEFGAB'[i%7] + str(i//7), origin=(dx*i+5.0, 5.0)) # Note label TODO: Calculate offsets properly
		# 	if i not in (2, 6):
		# 		# Accidental
		# 		polygon(octave, 0xFF0000, self.translate(dx*i+5.0, 0.0+5.0, black))
		# 		aalines(octave, (0,0,0), True, self.translate(dx*i+5.0, 0.0+5.0, black), 2)

		# drawKey(s, whiteM)
		# drawKey(s, translate(dx+5, 0, whiteL))
		# drawKey(s, translate((dx+5)*2, 0, whiteR))

		# surface.blit(s, (10,10))
		# self.surface.blit(octave, (0,0))
		return [Key(i, (dx, dy), (bdx, bdy)) for i in range(88)]


	def playChord(self, chord, fill=(210, 190, 50)):
		
		'''
		Docstring goes here
	
		'''

		for note in chord:
			self.key(note).play(fill=fill)
		self.update()



def main():
	
	'''
	Test suite

	'''

	pygame.init()
	piano = Piano()



if __name__ == '__main__':
	main()