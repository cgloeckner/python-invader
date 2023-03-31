import pygame

import settings
import resources
import game_object
import bullet
import powerup


player = None


def create(posx, posy):
	global player
	
	player = game_object.create(posx, posy, 'spaceship', settings.PLAYER_MOVE_SPEED, settings.PLAYER_MAX_HITPOINTS)
	
	player['shoot_cooldown'] = 0


def on_powerup(pup):
	player['hits'] += 1
	
	heal_sfx = resources.get_sound('powerup.ogg')
	heal_sfx.play()


def update():
	if player is None:
		return

	# Richtungsvektor zur Maus hin berechnen
	mouse_pos = pygame.mouse.get_pos()
	move = pygame.math.Vector2(mouse_pos) - player['pos']
	if move.length() > 5:
		player['move'] = move.normalize()
	else:
		player['move'] = pygame.math.Vector2(0, 0)
	
	# auf linke Mausklicks reagieren
	left_click = pygame.mouse.get_pressed()[0]
	if left_click and player['shoot_cooldown'] == 0:
		bullet.create(player)

	if player['shoot_cooldown'] > 0:
		player['shoot_cooldown'] -= 1

	# Powerup?
	for pup in powerup.all_powerups:
		if game_object.does_collide(player, pup):
			on_powerup(pup)
			powerup.remove(pup)

