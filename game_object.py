import pygame

import resources
import settings
import effect


all_objects = []
destroyed = []


def is_inside_screen(pos):
	if pos.x < 16 or pos.y < 16 or pos.x >= settings.WIDTH - 16 or pos.y >= settings.HEIGHT - 16:
		return False
	
	return True


def get_centered_pos(data):
	size = data['image'].get_height()
	center = pygame.math.Vector2(data['pos'])
	center.x -= size // 2
	center.y -= size // 2
	
	return center


def get_clipping_rect(data):
	# Frame Index aus Bewegung ableiten
	frame_index = 0
	
	if data['move'].x > 0:
		frame_index = 2
	elif data['move'].x < 0:
		frame_index = 1

	# Annahme: Frame-Größe ist quadratisch
	size = data['image'].get_height()
	clip = pygame.Rect(size * frame_index, 0, size, size)
	
	return clip


def create(posx, posy, image_filename, speed, hits):
	data = {}
	data['pos']     = pygame.math.Vector2(posx, posy)
	data['move']    = pygame.math.Vector2(0, 0)
	data['image']   = resources.get_image(image_filename + '.png')
	data['speed']   = speed
	data['radius']  = data['image'].get_height() // 2
	data['hits']    = hits
	data['max_hits'] = hits
	
	all_objects.append(data)
	
	return data


def remove(data):
	if data not in destroyed:
		destroyed.append(data)


def does_collide(obj, point):
	distance = pygame.math.Vector2.distance_to(obj['pos'], point['pos'])
	
	return distance < obj['radius']


def on_hit(data):
	data['hits'] -= 1
	effect.create(data)
	sfx_name = 'hit'
	
	if data['hits'] == 0:
		remove(data)
		sfx_name = 'explosion'
		
	sfx = resources.get_sound(sfx_name + '.ogg')
	sfx.play()


def update(data):
	new_pos = data['pos'] + data['move'] * data['speed']
	
	if is_inside_screen(new_pos):
		data['pos'] = new_pos
	else:
		# Bewegung stoppen
		data['move'] = pygame.math.Vector2(0, 0)


def draw(screen, data):
	center = get_centered_pos(data)
	clip = get_clipping_rect(data)
	
	pygame.Surface.blit(screen, data['image'], center, clip)


def draw_hitpoints(screen, data):
	pos = get_centered_pos(data)
	size = data['image'].get_height()
	
	percent = data['hits'] / data['max_hits']
	rect = pygame.Rect(pos.x, pos.y + size, size * percent, size // 8)
	
	pygame.draw.rect(screen, 'red', rect)


def draw_hitbox(screen, data):
	size = data['image'].get_height()
	rect = pygame.Rect(
		data['pos'].x - data['radius'],
		data['pos'].y - data['radius'],
		2 * data['radius'],
		2 * data['radius']
	)
	pygame.draw.arc(screen, 'yellow', rect, 0, 2 * 3.14)


def update_all():
	for data in all_objects:
		update(data)


def draw_all(screen, show_hitboxes=False):
	for data in all_objects:
		draw(screen, data)
		
		# Lebensbalken zeichnen
		if data['max_hits'] > 0:
			draw_hitpoints(screen, data)

	
	if show_hitboxes:
		for data in all_objects:
			draw_hitbox(screen, data)

