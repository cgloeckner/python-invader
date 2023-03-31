import random
import pygame

import settings
import resources
import game_object
import player


all_bullets = list()


def create(parent):
	from_player = parent == player.player

	# Position übernehmen
	pos = pygame.math.Vector2(parent['pos'])
	size = parent['image'].get_height() 
	pos.y += size
	if from_player:
		pos.y -= size * 2
	
	# Objekt erzeugen
	data = game_object.create(pos.x, pos.y, 'laser', 10, 0)
	data['radius'] = 0
	
	# Cooldown setzen
	if from_player:
		parent['shoot_cooldown'] = settings.PLAYER_SHOOT_COOLDOWN
	else:
		parent['shoot_cooldown'] = settings.ENEMY_SHOOT_COOLDOWN
	
	# Bewegungsrichtung anpassen
	data['move'].y = 1
	if from_player:
		data['move'].y = -1
	
	all_bullets.append(data)
	
	sfx = resources.get_sound('laser.ogg')
	sfx.play()
	
	return data


def remove(data):
	all_bullets.remove(data)
	game_object.all_objects.remove(data)


def update(data):
	if data['move'] == pygame.math.Vector2(0, 0):
		remove(data)

	# Teste ob etwas getroffen wurde
	did_hit = False
	for obj in game_object.all_objects:
		if obj in all_bullets:
			# keine Kollision mit Effekten oder Geschossen
			continue
  
		if game_object.does_collide(obj, data):
			game_object.on_hit(obj)
			did_hit = True

	if did_hit:
		remove(data)


def update_all():
	for data in all_bullets:
		update(data)

