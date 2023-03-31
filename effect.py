import pygame

import settings
import resources


all_effects = list()


def create(parent):
	# KEIN Game Object!
	data = {}
	data['parent'] = parent
	data['image']  = resources.get_image('explosion.png')
	
	data['animation_index'] = 0
	data['frame_delay']     = settings.EXPLOSION_ANI_DELAY
	
	all_effects.append(data)
	
	return data


def remove(data):
	all_effects.remove(data)


def update(data):
	data['frame_delay'] -= 1
	
	if data['frame_delay'] == 0:
		data['animation_index'] += 1
		data['frame_delay'] = settings.EXPLOSION_ANI_DELAY
	
	size = data['image'].get_size()
	if data['animation_index'] >= size[0] // size[1]:
		remove(data)


def update_all():
	for data in all_effects:
		update(data)


def draw(screen, data):
	# Position zentrieren (mit Kopie des Vektors)
	parent = data['parent']
	size = parent['image'].get_height()
	center = pygame.math.Vector2(parent['pos'])
	center.x -= size // 2
	center.y -= size // 2
	
	clip = pygame.Rect(size * data['animation_index'], 0, size, size)
	
	pygame.Surface.blit(screen, data['image'], center, clip)


def draw_all(screen):
	for data in all_effects:
		draw(screen, data)


