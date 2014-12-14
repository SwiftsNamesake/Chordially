#
# Chordially - Key.py
# Implements a Key class
#
# Jonatan H Sundqvist
# December 13 2014
#

# TODO | - 
#        -
#
# SPEC | -
#        -



import pygame
from SwiftUtils.MultiSwitch import MultiSwitch
from utilities import debug



class Key(object):

	'''
	Docstring goes here

	'''

	WHITE  = 0
	BLACK  = 1
	LEFT   = 2
	RIGHT  = 4
	MIDDLE = 5 # TODO: Rename BOTH (?)

	# Table of conversion functions TO an index
	conversions = {
		int: 	lambda self, k: k,								 		# Index (eg. 5)
		tuple:  lambda self, k: (k[1]-1)*7 + 'CDEFGAB'.index(k[0]), 	# (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
		str:	lambda self, k: (int(k[1]))*7 + 'CDEFGAB'.index(k[0]) # Note name (eg. 'G2') (forgive me Father, for I have recursed)
	}

	# Table of conversion functions FROM an index
	# TODO: Break out some general functionality (?)
	# TODO: Tuple conversion can probably be simplified by recognizing the pattern (cf. self.note)
	aliases = {
		int: 	lambda self, k: k,						 		 	# Index (eg. 5)
		tuple:  lambda self, k: (self.note(k), self.octave(k)), 	# (Note, Octave) (eg. ('A', 3)) # TODO: Fix alignment
		str:	lambda self, k: self.note(k) + str(self.octave(k)) 	# Note name (eg. 'G2') (forgive me Father, for I have recursed)
	}

	lazy = lambda code, capture='': eval('lambda {}: {}'.format(code, capture))

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

		self.vertices = self.makeVertices(self.sizeWhite, self.sizeBlack) # Vertices

		self.fill = ((255, 255, 255) if self.kind is self.WHITE else (0, 0, 0))  # Fill colour
		self.font = pygame.font.SysFont('Tahoma', 22)							 # Label font


	def normalize(self, key):
		# Converts to an index
		return self.alias(key, to=int)


	def note(self, key):
		# TODO: Use string as key instead, would probably be more legible (?)
		assert isinstance(key, int)
		return 'CDEFGAB'[MultiSwitch({
			(0,1): 0,
			(2,3): 1,
			(4,): 2,
			(5,6): 3,
			(7,8): 4,
			(9,10): 5,
			(11,): 6})[key%12]] # TODO: Take offset and accidentals into account


	def octave(self, key):
		assert isinstance(key, int)
		return key//12 # TODO: Take offset into account


	def alias(self, key, to=int):
		# Converts between different representations (aliases) of a key
		# NOTE: Currently, this method will always return an index (int)
		# TODO: Implement multi-way mapping or translation (maybe via an A to B to C and C to B to A scheme)
		# TODO: More elegant scheme for lazy evaluation (?)
		debug('key={!r}, to={!r}'.format(key, to))
		index = self.conversions[type(key)](self, key)
		debug('Index of %r is %d' % (key, index))
		return self.aliases[to](self, index)


	def findKind(self):
		# TODO: Take offset (self.start) into account
		return self.WHITE if self.index % 12 in (0, 2, 4, 5, 7, 9, 11) else self.BLACK


	def findShape(self):
		return MultiSwitch({ (0,5): self.RIGHT, (2,7,9): self.MIDDLE, (4,11): self.LEFT }).get(self.index % 12, self.BLACK) # TODO: Implement MultiDict (?)


	def __str__(self):
		return self.name


	def __repr__(self):
		return 'Key(index={.index}, name={.name}, type={.type}'.format(self)


	def makeVertices(self, sizeWhite, sizeBlack):
		# 
		dx, dy, bdx, bdy = sizeWhite + sizeBlack # Unpack widths and heights
		middle 	= [(0.0, dy), (dx, dy), (dx, bdy), (dx-bdx/2, bdy), (dx-bdx/2, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)]	# 
		return {
			self.BLACK: self.translate(dx-bdx/2, 0.0,[(0.0, 0.0), (bdx, 0.0), (bdx, bdy), (0.0, bdy)]),	#
			self.LEFT: 	middle[:2] + [(dx, 0.0), (bdx/2, 0.0), (bdx/2, bdy), (0.0, bdy)],				#
			self.MIDDLE: middle,																		#
			self.RIGHT:  middle[:5] + [(0.0, 0.0), (0.0, dy)]											#
		}[self.shape]


	def resize(self, sizeWhite, sizeBlack):
		# 
		self.sizeWhite  = sizeWhite
		self.sizeBlack 	= sizeBlack
		self.vertices 	= self.makeVertices(self.sizeWhite, self.sizeBlack)


	def origin(self, absolute=(0,0)):
		# Relative coordinates of the key's origin (top left corner)
		return absolute[0]+self.sizeWhite[0]*(self.octave(self.index)*7+'CDEFGAB'.index(self.name[0])), absolute[1]


	def inside(self, x, y):
		# Deterimines if a point lies on the key
		return False # TODO: Implement (duh)


	def render(self, surface, outline=(0,0,0), origin=(0,0), labelled=False):
		# TODO: Cache translation (?)
		# TODO: Key.offset utility method
		# if self.kind==self.BLACK: pass
		dx, dy, bdx, bdy = self.sizeWhite + self.sizeBlack # Unpack widths and heights
		debug('Octave of %s is %d' % (self, self.octave(self.index)))
		debug('Horizontal offset is %d\n' % (dx*self.octave(self.index)*7))
		corner = self.origin(origin)
		vertices = self.translate(corner[0], corner[1], self.vertices)
		pygame.draw.polygon(surface, self.fill, vertices)
		pygame.draw.aalines(surface, outline, True, vertices, True)
		if labelled:
			self.label(surface, origin=corner)


	def translate(self, dx, dy, vertices):
		return [(vtx[0]+dx, vtx[1]+dy) for vtx in vertices]


	def label(self, surface, fill=(255, 20, 20), pady=5.0, origin=(0,0)):
		# TODO: Refactor, clarify and comment the position calculations (?)
		# TODO: Fix origin
		dx, dy, bdx, bdy = self.sizeWhite + self.sizeBlack # Unpack widths and heights
		text = self.font.render(self.name, 2, fill) # Label text, anti-alias, fill colour
		surface.blit(text, (origin[0]+(dx-text.get_size()[0])/2, origin[1]+dy-text.get_size()[1]-pady))


	def play(self, fill=(210, 190, 50), duration=None):

		'''
		Docstring goes here

		'''

		self.oldfill = self.fill # Save current fill colour so that that it can be restored later (when the key is released)
		self.fill = fill
		if duration is not None:
			pass

		# raise NotImplementedError('No audio for now I\'m afraid. Sincere apologies.')


def main():
	
	'''
	Test suite
	
	'''

	pygame.init()
	keys = [Key('C4', (20, 40), (10, 18))]
	# piano = Piano()



if __name__ == '__main__':
	main()