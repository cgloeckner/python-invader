import random
import math
import pygame

import settings
import game_object
import bullet
import powerup
import player
import wave


all_enemies = list()


def create(posx, posy, move_speed, max_hitpoints, max_shoot_cooldown):
	data = game_object.create(posx, posy, 'ufo', move_speed, max_hitpoints)
	
	data['hover_animation'] = 0
	data['shoot_cooldown'] = 0
	data['max_shoot_cooldown'] = max_shoot_cooldown
	
	change_direction(data)
	
	all_enemies.append(data)
	
	return data


def on_destroy(data):
	if random.random() > 0.5:
		powerup.create(data)
	
	wave.on_score()
	

def change_direction(data):
	# zufällige L/R-Bewegung (oder stehen)
	data['move'].x = random.randrange(3) - 1
	
	# für einige Durchläufe so bewegen
	data['move_counter'] = 10 * (3 + random.randrange(4))		


def animate_hovering(data):
	angle = 2 * math.pi * data['hover_animation'] / 100
	data['pos'].y += math.sin(angle)
	data['hover_animation'] += 1


def update(data):
	data['move_counter'] -= 1
	
	# zufällige Bewegung einschlagen
	if data['move_counter'] == 0:
		change_direction(data)

	# Feuern?
	if data['move'].x == 0 and data['shoot_cooldown'] == 0 and player.player is not None:
		bullet.create(data)
	
	if data['shoot_cooldown'] > 0:
		data['shoot_cooldown'] -= 1

	animate_hovering(data)


def update_all():
	for data in all_enemies:
		update(data)

