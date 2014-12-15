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


	def tick(self):

		'''
		Docstring goes here

		'''

		self.canvas.fill(((0, 72, 50), (0xFF, 0xFF, 0), colours['BG'])[2])
		self.piano.render(surface, (20, 20))
		pygame.display.flip()
		self.clock.tick(60)


	def run(self):

		'''
		Docstring goes here

		'''

		self.mainloop()



def createContext(size):

	'''
	Docstring goes here

	'''

	pygame.init()
	surface = pygame.display.set_mode(size)
	pygame.display.set_caption('Chordially')
	clock = pygame.time.Clock()

	return Context(surface, size, EventDispatcher(), clock)


def tick(dt, ctx, world):
	
	'''
	Docstring goes here

	'''

	surface = ctx.surface
	θ = 0.0

	p = lambda sides: [(160+60*(sin(θ)+1.5)*cos(θ+s*2*π/sides)+250, 160+60*(sin(θ)+1.5)*sin(θ+s*2*π/sides)+20) for s in range(sides)]

	surface.fill(((0, 72, 50), (0xFF, 0xFF, 0), colours['BG'])[2])

	world.piano.render(surface, (20, 20))
	pygame.draw.aalines(surface, ((255+255*cos(θ))//2, (255+255*sin(θ))//2, 0xF9), True, p(10), False)

	pygame.display.flip()
	ctx.clock.tick(60)



def main():
	
	'''
	Docstring goes here

	'''

	# Initialize basic components (pygame, events, window)
	# ctx = createContext((720*2, 480))
	
	# # Setup
	# mFont = pygame.font.SysFont('oldenglishtext', 20)
	# world = namedtuple('Word', 'piano')(Piano())

	# # Events
	# ctx.events.always = lambda dt: tick(dt, ctx, world)
	# ctx.events.bind({'type': KEYDOWN, 'mod': 1}, lambda p, e: print('Hello'))
	# ctx.events.bind({'type': KEYDOWN, 'key': K_ESCAPE}, lambda p, e: pygame.quit())
	# ctx.events.bind({'type': KEYDOWN, 'key': K_SPACE, 'doc': 'Play an F chord'}, lambda p, e: (print(p.doc), world.piano.playChord((5, 9, 12))))
	# ctx.events.bind({'type': KEYUP, 'key': K_SPACE}, lambda p, e: world.piano.playChord((5, 9, 12), fill=(255, 255, 255)))

	# ctx.events.mainloop()

	app = Application('Chordially', (720*2, 480))
	app.run()


if __name__ == '__main__':
	main()