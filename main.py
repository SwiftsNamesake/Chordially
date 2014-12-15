#
# Chordially - main.py
# Visualizing music theory, focusing on piano chords
#
# Jonatan H Sundqvist
# December 12 2014
#

# TODO | - App class (?)
#        -
#
# SPEC | -
#        -



from collections import namedtuple

import pygame
from pygame.locals import *
from SwiftUtils.EventDispatcher import EventDispatcher
from SwiftUtils.MultiSwitch import MultiSwitch

from math import sin, cos, e, pi as π

from Piano import Piano
from Chords import Chords
from utilities import debug



Context = namedtuple('Context', 'surface size events clock')
colours = {
	'BG': 	(39, 40, 34),		# Background
	'DEF': 	(102, 217, 239),	# Def keyword
	'ARG': 	(253, 151, 32),		# Argument
	'OP': 	(249, 39,  114),	# Operator
	'LIT': 	(141, 129, 255),	# Literal
	'STR': 	(230, 219, 116),	# String
	'VAR': 	(248, 248, 242),	# Variable
	'FUN': 	(166, 182, 36),		# Function name
	'COM': 	(107, 113, 94),		# Comment
	'WHITE': (255, 255, 255),	#
	'BLACK': (0, 0, 0)			#
}



class Application(EventDispatcher):

	'''
	Docstring goes here

	'''

	def __init__(self, title, size, resizable=True):
		
		'''
		Docstring goes here

		'''

		# 
		super().__init__()

		# Initialize basics
		pygame.init()
		self.canvas = pygame.display.set_mode(size)
		pygame.display.set_caption(title)
		self.clock = pygame.time.Clock()

		# App data
		self.piano = Piano()

		# Events
		self.bindEvents()


	def bindEvents(self):

		'''
		Docstring goes here

		'''
		
		self.always = lambda dt: self.tick(dt)
		self.bind({'type': KEYDOWN, 'mod': 1}, lambda p, e: print('Hello'))
		self.bind({'type': KEYDOWN, 'key': K_ESCAPE}, lambda p, e: pygame.quit())
		self.bind({'type': KEYDOWN, 'key': K_SPACE, 'doc': 'Play an F chord'}, lambda p, e: (print(p.doc), self.piano.playChord((5, 9, 12))))
		self.bind({'type': KEYUP, 'key': K_SPACE}, lambda p, e: self.piano.playChord((5, 9, 12), fill=(255, 255, 255)))


	def tick(self, dt):

		'''
		Docstring goes here

		'''

		self.canvas.fill(((0, 72, 50), (0xFF, 0xFF, 0), colours['BG'])[2])
		self.piano.render(self.canvas, (20, 20))
		pygame.display.flip()
		self.clock.tick(60)


	def run(self):

		'''
		Docstring goes here

		'''

		self.mainloop()



def main():
	
	'''
	Docstring goes here

	'''

	app = Application('Chordially', (720*2, 480))
	app.run()


if __name__ == '__main__':
	main()