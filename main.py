#
# Chordially - main.py
# Visualizing music theory, focusing on piano chords
#
# Jonatan H Sundqvist
# December 12 2014
#

# TODO | -
#        -
#
# SPEC | -
#        -



import pygame
from collections import namedtuple
from pygame.locals import *
from SwiftUtils.EventDispatcher import EventDispatcher
from math import sin, cos, pi as π


_print = print
def addLine(*args, **kwargs):
	# Dangerous hack
	from inspect import getouterframes, currentframe, getframeinfo
	caller = getframeinfo(currentframe().f_back)
	_print(caller)
	_print('[{0.lineno}]'.format(caller), end=' ')
	_print(*args, **kwargs)

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


def createContext(size):

	'''
	Docstring goes here

	'''

	pygame.init()
	surface = pygame.display.set_mode(size)
	clock = pygame.time.Clock()

	return Context(surface, size, EventDispatcher(), clock)



def piano(surface):
	
	'''
	Renders an 88-key piano

	'''

	# TODO: Options
	# TODO: Animation
	# TODO: Wavefront 3D model
	# TODO: Padding
	# TODO: Individually accessible keys, colour changes

	'''
	def getKey(key):
		return {
			int: 	self.keys[key],									# Index (eg. 5)
			tuple:  self.keys[(key[1]-1)*7 + ord(key[0])-ord('A')] 	# (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
			str:	self.getKey((key[0], int(key[1]))) 				# Note name (eg. 'G2') (forgive me Father, for I have recursed)
		}[type(key)]
	'''

	dx = 2.0  * 20 # Width of a white key
	dy = 13.5 * 20 # Height of a white key

	bdx = 1.2*20 # Width of a black key
	bdy = 8.5*20 # Height of a black key
	
	# pygame.draw.polygon(surface, colour, vertices, width)
	s = pygame.Surface((10*(dx+5), dy)) # Temporary surface

	def translate(dx, dy, vertices):
		return [(vtx[0]+dx, vtx[1]+dy) for vtx in vertices]

	def drawKey(surf, vertices, fill=0xFFFFFF, outline=(0, 0, 0), surface=s, cycle=True, width=8):
		polygon(surf, fill, vertices)
		aalines(surf, outline, True, vertices, width)


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
	whiteM = [(0.0, dy), (dx, dy), (dx, bdy), (dx-bdx/2, bdy), (dx-bdx/2, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)] # Middle white
	whiteL = whiteM[:2] + [(dx, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)] 											# White with left inset
	whiteR = whiteM[:5] + [(0.0, 0.0), (0.0, dy)] 																		# White with right inset

	black = translate(dx-bdx/2, 0.0, [(0.0, 0.0), (bdx, 0.0), (bdx, bdy), (0.0, bdy)])

	polygon = pygame.draw.polygon
	aalines = pygame.draw.aalines

	s.fill(colours['BG'])

	octave = pygame.Surface((dx*7+10, dy+10))

	for i in range(7):
		drawKey(octave, translate(dx*i, 0, [whiteR, whiteM, whiteL, whiteR, whiteM, whiteM, whiteL][i]))
		if i not in (2, 6):
			polygon(octave, 0xFF0000, translate(dx*i, 0.0, black))

	# drawKey(s, whiteM)
	# drawKey(s, translate(dx+5, 0, whiteL))
	# drawKey(s, translate((dx+5)*2, 0, whiteR))

	surface.blit(s, (10,10))
	surface.blit(octave, (10,10))

	for i in range(88):
		pass



def tick(dt, ctx):
	
	'''
	Docstring goes here

	'''

	surface = ctx.surface
	θ = 0.0

	surface.fill(((0, 72, 50), (0xFF, 0xFF, 0), colours['BG'])[2])
	pygame.draw.aalines(surface, ((255+255*cos(θ))//2, (255+255*sin(θ))//2, 0xF9), True, (lambda sides: [(160+60*(sin(θ)+1.5)*cos(θ+s*2*π/sides),
																		  160+60*(sin(θ)+1.5)*sin(θ+s*2*π/sides)) for s in range(sides)])(10), 5)

	piano(surface)

	pygame.display.flip()
	ctx.clock.tick(60)



def main():
	
	'''
	Docstring goes here

	'''

	# Initialize basic components (pygame, events, window)
	ctx = createContext((720, 480))
	
	# Setup
	mFont = pygame.font.SysFont('oldenglishtext', 20)

	# Events
	ctx.events.always = lambda dt: tick(dt, ctx)
	ctx.events.bind({'type': KEYDOWN, 'mod': 1}, lambda e: print('Hello'))
	ctx.events.bind({'type': KEYDOWN, 'key': K_ESCAPE}, quit)

	ctx.events.mainloop()



if __name__ == '__main__':
	main()