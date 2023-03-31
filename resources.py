import pygame


all_images = {}
all_sounds = {}


def get_image(filename):
	if filename not in all_images:
		original = pygame.image.load(filename)
		doubled  = pygame.transform.scale2x(original)
		all_images[filename] = doubled
	
	return all_images[filename]


def get_sound(filename):
	if filename not in all_sounds:
		sound = pygame.mixer.Sound(filename)
		all_sounds[filename] = sound
	
	return all_sounds[filename]

