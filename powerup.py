import pygame

import settings
import resources


all_powerups = list()


def create(parent):
	# KEIN Game Object!
	data = {}
	data['pos']   = pygame.math.Vector2(parent['pos'])
	data['image'] = resources.get_image('powerup.png')
	
	all_powerups.append(data)
	
	return data


def remove(data):
	all_powerups.remove(data)


def draw(screen, data):
	# Position zentrieren (mit Kopie des Vektors)
	size = data['image'].get_height()
	center = pygame.math.Vector2(data['pos'])
	center.x -= size // 2
	center.y -= size // 2
	
	pygame.Surface.blit(screen, data['image'], center)


def draw_all(screen):
	for data in all_powerups:
		draw(screen, data)


