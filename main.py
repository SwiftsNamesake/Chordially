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
from SwiftUtils.MultiSwitch import MultiSwitch
from math import sin, cos, pi as π


_print = print
def addLine(*args, **kwargs):
	# Dangerous hack
	from inspect import getouterframes, currentframe, getframeinfo
	caller = getframeinfo(currentframe().f_back)
	_print('[{0.lineno}]'.format(caller), end=' ')
	_print(*args, **kwargs)
print = addLine

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



class Piano(object):

	'''
	Renders an 88-key piano

	'''
	
	class Key(object):

		WHITE  = 0
		BLACK  = 1
		LEFT   = 2
		RIGHT  = 4
		MIDDLE = 5

		# Table of conversion functions TO an index
		conversions = {
			int: 	lambda self, k: k,								 # Index (eg. 5)
			tuple:  lambda self, k: (k[1]-1)*7 + ord(k[0])-ord('A'), # (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
			str:	lambda self, k: self.alias((k[0], int(k[1]))) 	 # Note name (eg. 'G2') (forgive me Father, for I have recursed)
		}

		# Table of conversion functions FROM an index
		# TODO: Break out some general functionality (?)
		# TODO: Tuple conversion can probably be simplified by recognizing the pattern
		aliases = {
			int: 	lambda self, k: k,						 		 # Index (eg. 5)
			tuple:  lambda self, k: (self.note(), self.octave()), 	 # (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
			str:	lambda self, k: self.note() + str(self.octave()) # Note name (eg. 'G2') (forgive me Father, for I have recursed)
		}

		# TODO: Static utility methods (?)

		# self.drawKey(octave, self.translate(dx*i+5.0, 5.0, [whiteR, whiteM, whiteL, whiteR, whiteM, whiteM, whiteL][i])) # Whole note
		# self.drawLabel(octave, 'CDEFGAB'[i%7] + str(i//7), origin=(dx*i+5.0, 5.0)) # Note label TODO: Calculate offsets properly

		# def noteLabel(self, key, fill=(0,0,0), font=('Tahoma', 22)):
			# return pygame.font.SysFont(*font).render(key, 2, fill) # Text, anti-alias, color, background=None

		# def drawLabel(self, surf, key, origin=(0,0), fill=(0,0,0), pady=5.0, font=('Tahoma', 22)):
			# TODO: Refactor, clarify and comment the position calculations (?)
			# label = pygame.font.SysFont(*font).render(key, 2, fill)
			# surf.blit(label, (origin[0]+(self.dx-label.get_size()[0])/2, origin[1]+self.dy-label.get_size()[1]-pady))

		def __init__(self, which, sizeWhite, sizeBlack, first='C0'):
			#
			self.first = self.normalize(first) # First (leftmost) key (useful for calculating indeces)
			self.index = self.normalize(which) # Index of the key in a standard 88-key piano
			self.name  = self.alias(which, to=str)

			# self.kind = { self.name[0] in } # Which kind of note is it? (TODO: Split colour and shape into separate attributes?)
			self.shape = self.findShape()
			self.kind  = self.findKind()

			#
			self.sizeWhite = sizeWhite # Size of a white key
			self.sizeBlack = sizeBlack # Size of a black key

			self.vertices = self.makeVertices(sizeWhite, sizeBlack) # Vertices

			self.fill = ((255, 255, 255) if self.kind is self.WHITE else (0, 0, 0))  # Fill colour
			self.font = pygame.font.SysFont('Tahoma', 22)							 # Label font

		def normalize(self, key):
			return self.alias(key, to=int)

		def note(self):
			return 'CDEFGAB'[MultiSwitch((0, 1): 0, (): 1, (): 2, (): 3, (): 4, (): 5, (): 6)[k%12]] # TODO: Take offset and accidentals into account

		def octave(self):
			return self.index//12 # TODO: Take offset into account

		def alias(self, key, to=int):
			# Converts between different representations (aliases) of a key
			# NOTE: Currently, this method will always return an index (int)
			# TODO: Implement multi-way mapping or translation (maybe via an A to B to C and C to B to A scheme)
			# TODO: More elegant scheme for lazy evaluation (?)
			print('key={!r}, to={!r}'.format(key, to))
			index = self.conversions[type(key)](self, key) 
			return self.aliases[type(key)](self, key)

		def findKind(self):
			# TODO: Take offset (self.start) into account
			return self.WHITE if self.index % 12 in (0, 2, 4, 5, 7, 9, 11) else self.BLACK

		def findShape(self):
			return MultiSwitch({ (0,5): self.RIGHT, (2,7,9,5): self.MIDDLE, (4,11): self.LEFT }).get(self.index % 12, self.BLACK) # TODO: Implement MultiDict (?)

		def __str__(self):
			return self.name

		def __repr__(self):
			return 'Key(index={.index}, name={.name}, type={.type}'.format(self)

		def makeVertices(self, sizeWhite, sizeBlack):
			dx, dy, bdx, bdy = sizeWhite + sizeBlack # Unpack widths and heights
			middle 	= [(0.0, dy), (dx, dy), (dx, bdy), (dx-bdx/2, bdy), (dx-bdx/2, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)]	# 
			return {
				self.BLACK: [(0.0, 0.0), (bdx, 0.0), (bdx, bdy), (0.0, bdy)],					#
				self.LEFT: 	middle[:2] + [(dx, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)],	#
				self.MIDDLE: middle,															#
				self.RIGHT:  middle[:5] + [(0.0, 0.0), (0.0, dy)]								#
			}[self.shape]

		def resize(self, sizeWhite, sizeBlack):
			self.sizeWhite  = sizeWhite
			self.sizeBlack = sizeBlack
			self.vertices = self.makeVertices(self.sizeWhite, self.sizeBlack)

		def inside(self, x, y):
			# Deterimines if a point lies on the key
			return False # TODO: Implement (duh)

		def render(self, surface, fill=0xFFFFFF, outline=(0,0,0), cycle=True, width=8):
			pygame.draw.polygon(surface, fill, self.vertices)
			pygame.draw.aalines(surface, outline, True, self.vertices, width)

		def label(self, surface, fill=(255, 20, 20), pady=5.0):
			# TODO: Refactor, clarify and comment the position calculations (?)
			origin = (0,0) # TODO: Fix origin
			dx, dy, bdx, bdy = sizeWhite + sizeBlack # Unpack widths and heights
			text = self.font.render(self.name, 2, fill)
			surface.blit(text, (origin[0]+(dx-text.get_size()[0])/2, origin[1]+dy-text.get_size()[1]-pady))

		def play(self):
			pass


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

		
	def render(self, surface, position):

		'''
		Docstring goes here

		'''

		surface.blit(self.surface, position)


	def key(self, key):
		return {
			int: 	self.keys[key],									# Index (eg. 5)
			tuple:  self.keys[(key[1]-1)*7 + ord(key[0])-ord('A')], # (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
			str:	self.key((key[0], int(key[1]))) 				# Note name (eg. 'G2') (forgive me Father, for I have recursed)
		}[type(key)]


	def translate(self, dx, dy, vertices):
		return [(vtx[0]+dx, vtx[1]+dy) for vtx in vertices]


	def drawKey(self, surf, vertices, fill=0xFFFFFF, outline=(0,0,0), cycle=True, width=8):
		pygame.draw.polygon(surf, fill, vertices)
		pygame.draw.aalines(surf, outline, True, vertices, width)


	def noteLabel(self, key, fill=(0,0,0), font=('Tahoma', 22)):
		return pygame.font.SysFont(*font).render(key, 2, fill) # Text, anti-alias, color, background=None


	def drawLabel(self, surf, key, origin=(0,0), fill=(0,0,0), pady=5.0, font=('Tahoma', 22)):
		# TODO: Refactor, clarify and comment the position calculations (?)
		label = pygame.font.SysFont(*font).render(key, 2, fill)
		surf.blit(label, (origin[0]+(self.dx-label.get_size()[0])/2, origin[1]+self.dy-label.get_size()[1]-pady))


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
		whiteM = [(0.0, dy), (dx, dy), (dx, bdy), (dx-bdx/2, bdy), (dx-bdx/2, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)] # Middle white
		whiteL = whiteM[:2] + [(dx, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)] 											# White with left inset
		whiteR = whiteM[:5] + [(0.0, 0.0), (0.0, dy)] 																		# White with right inset

		black = self.translate(dx-bdx/2, 0.0, [(0.0, 0.0), (bdx, 0.0), (bdx, bdy), (0.0, bdy)])

		polygon = pygame.draw.polygon
		aalines = pygame.draw.aalines

		# s.fill(colours['BG'])

		octave = pygame.Surface((dx*7+10, dy+10))

		for i in range(7):
			self.drawKey(octave, self.translate(dx*i+5.0, 5.0, [whiteR, whiteM, whiteL, whiteR, whiteM, whiteM, whiteL][i])) # Whole note
			self.drawLabel(octave, 'CDEFGAB'[i%7] + str(i//7), origin=(dx*i+5.0, 5.0)) # Note label TODO: Calculate offsets properly
			if i not in (2, 6):
				# Accidental
				polygon(octave, 0xFF0000, self.translate(dx*i+5.0, 0.0+5.0, black))
				aalines(octave, (0,0,0), True, self.translate(dx*i+5.0, 0.0+5.0, black), 2)

		# drawKey(s, whiteM)
		# drawKey(s, translate(dx+5, 0, whiteL))
		# drawKey(s, translate((dx+5)*2, 0, whiteR))

		# surface.blit(s, (10,10))
		self.surface.blit(octave, (0,0))
		return [Piano.Key(i, (dx, dy), (bdx, bdy)) for i in range(88)]



def tick(dt, ctx):
	
	'''
	Docstring goes here

	'''

	surface = ctx.surface
	θ = 0.0

	p = lambda sides: [(160+60*(sin(θ)+1.5)*cos(θ+s*2*π/sides)+250, 160+60*(sin(θ)+1.5)*sin(θ+s*2*π/sides)+20) for s in range(sides)]

	surface.fill(((0, 72, 50), (0xFF, 0xFF, 0), colours['BG'])[2])

	Piano().render(surface, (20, 20))
	pygame.draw.aalines(surface, ((255+255*cos(θ))//2, (255+255*sin(θ))//2, 0xF9), True, p(10), False)

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
	ctx.events.bind({'type': KEYDOWN, 'key': K_ESCAPE}, lambda e: pygame.quit())

	ctx.events.mainloop()



if __name__ == '__main__':
	main()