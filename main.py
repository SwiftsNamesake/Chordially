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
from pygame.locals import *
from SwiftUtils.EventDispatcher import EventDispatcher



def createContext(size):

	'''
	Docstring goes here

	'''

	pygame.init()
	surface = pygame.display.set_mode(size)
	clock = pygame.time.Clock()

	return surface, clock



def tick(dt):
	
	'''
	Docstring goes here

	'''

	pass



def main():
	
	'''
	Docstring goes here

	'''

	# Initialize basic components (pygame, events, window)
	ctx = createContext((200, 200))
	evt = EventDispatcher() # Handles event dispatching
	
	# Setup
	mFont = pygame.font.SysFont('oldenglishtext', 20)

	# Events
	evt.always = tick
	evt.bind({'type': 0}, lambda e: print('Hello'))

	evt.mainloop()



if __name__ == '__main__':
	main()