#
# Chordially - main.py
# Visualizing music theory, focusing on piano chords
#
# Jonatan H Sundqvist
# December 12 2014
#

# TODO | - App class (?)
#        - Animation
#        - Implement testing for each component
#
# SPEC | -
#        -



from collections import namedtuple
from itertools import cycle, count

import pygame
from pygame.locals import *
from SwiftUtils.EventDispatcher import EventDispatcher

from math import sin, cos, e, pi as π #, sqrt as √
from random import choice, randint

from Piano import Piano
from Key import Key
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

	def __init__(self, title, size, resizable=True, icon=None):
		
		'''
		Docstring goes here

		'''

		# 
		super().__init__()

		# Initialize basic components
		pygame.init()

		# App data
		self.piano = Piano(scale=20, compass=('C0', 'C5'))
		width, height = self.piano.size()

		#
		self.canvas = pygame.display.set_mode((int(width)+2*20, int(height)+2*20)) #size
		pygame.display.set_caption(title)
		self.clock = pygame.time.Clock()

		# Events
		self.bindEvents()


	def bindEvents(self):

		'''
		Docstring goes here

		'''
		
		for key in ('C1', 'C2#', 'G3', 'G4', 'A4#'):
			assert key == self.piano.key(key).name, 'Key should be {} but is instead ({}, {}) ({}, {})'.format(key,
																										 self.piano.key(key).name, self.piano.key(key).index,
																										 self.piano.keyUtils.alias(key, to=str),
																										 self.piano.keyUtils.alias(key))
			print('Key {0} has index {1.index} and name {1.name}'.format(key, self.piano.key(key)))

		# print('C2: {}, F2: {}, G2: {}'.format(self.piano.key('C2').index, self.piano.key('F2').index, self.piano.key('G2').index))

		randColour = lambda: (randint(0,255), randint(0,255), randint(0,255))

		self.always = lambda dt: self.tick(dt)
		self.bind({'type': KEYDOWN, 'mod': 1}, 			lambda p, e: print('Hello'))
		self.bind({'type': KEYDOWN, 'key': K_ESCAPE}, 	lambda p, e: pygame.quit())
		self.bind({'type': KEYUP, 'key': K_SPACE}, 		lambda p, e: self.piano.releaseChord(Chords.G))
		self.bind({'type': KEYDOWN, 'key': K_SPACE, 'doc': 'Play an F chord'}, lambda p, e: self.piano.playChord(Chords.G))
		self.bind({'type': KEYDOWN, 'unicode': 'b'}, lambda p, e: self.piano.playChord(('C1', 'C2#', 'G3', 'G4', 'A4#'), fill=randColour()))
		self.bind({'type': MOUSEBUTTONDOWN, 'button': 1}, self.onLeftClick) # TODO: Fix hard-coding
		self.bind({'type': MOUSEMOTION}, self.onMove) # TODO: Fix hard-coding

	# fade = cycle(((min(int(r), 255), min(int(r), 255), min(int(r), 255)) for r in range(0, 1000, 1)))
	fade = ((126+125*sin(x*π/180.0), 126+125*cos(x*π/180.0), 126+125*sin(x*π/180.0)) for x in count(0))

	def tick(self, dt):

		'''
		Docstring goes here

		'''

		self.canvas.fill(((0, 72, 50), (0xFF, 0xFF, 0x0), colours['BG'])[2])

		self.piano.labelOptions['fill'] = next(self.fade)
		# fill = next(self.fade)
		# for key in self.piano.keys:
			# key.fill = fill
		self.piano.update()

		self.piano.render(self.canvas, (20, 20)) # TODO: Store position somewhere
		pygame.display.flip()
		self.clock.tick(60)

	def onMove(self, pattern, event):
		# TODO: Optimize
		# TODO: create equivalent Piano method (?)
		x, y = event.pos
		for key in self.piano.keys:
			if key.inside(x-20-10, y-20-10):
				# print('You clicked {!s}'.format(key))
				if hasattr(self, 'previous') and (self.previous != key):
					self.previous.release()
				if not hasattr(self, 'previous') or (self.previous != key):
					key.play(fill=(randint(0,255), randint(0,255), randint(0,255)))
				self.previous = key
				return



	def onLeftClick(self, pattern, event):
		x, y = event.pos
		for key in self.piano.keys:
			if key.inside(x-20-10, y-20-10):
				print('You clicked {!s}'.format(key))
				return


	def run(self):

		'''
		Docstring goes here

		'''

		self.mainloop()



def main():

	'''
	Docstring goes here

	'''

	app = Application('Chordially', (int(2.0*20*88*7/12) + 2 * 20, int(13.5*20) + 2 * 20))
	app.run()



if __name__ == '__main__':
	main()