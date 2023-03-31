import random
import pygame

import settings
import player
import enemy
import effect


next_wave_cooldown  = settings.WAVE_COOLDOWN
current_wave_number = 1

paused = False

ui_font = None
score = 0


def restart():
	global next_wave_cooldown
	global current_wave_number
	global score
	global paused
	
	next_wave_cooldown  = settings.WAVE_COOLDOWN
	current_wave_number = 1
	score = 0
	paused = False
	
	player.create(settings.WIDTH // 2, settings.HEIGHT - 50)


def on_score():
	global score
	
	score += 1


def end():
	global next_wave_cooldown
	global current_wave_number
	
	next_wave_cooldown  = settings.WAVE_COOLDOWN
	current_wave_number += 1


def new():
	global current_wave_number
	
	move_speed     = settings.ENEMY_MOVE_SPEED + current_wave_number % 3
	max_hitpoints  = settings.ENEMY_MAX_HITPOINS + current_wave_number % 5
	shoot_cooldown = settings.ENEMY_SHOOT_COOLDOWN - current_wave_number
	if shoot_cooldown < settings.PLAYER_SHOOT_COOLDOWN:
		shoot_cooldown = settings.PLAYER_SHOOT_COOLDOWN
	
	num_enemies = random.randrange(2, 5)
	i = 1
	while i < num_enemies:
		enemy.create(i * settings.WIDTH // num_enemies, 25 + i * 50, move_speed, max_hitpoints, shoot_cooldown)
		i += 1


def update():
	global next_wave_cooldown
	
	if len(enemy.all_enemies) == 0 and next_wave_cooldown == -1:
		end()
	
	if next_wave_cooldown == 0:
		new()
	
	if next_wave_cooldown >= 0:
		next_wave_cooldown -= 1


def draw(screen):
	global ui_font
	
	if ui_font is None:
		ui_font = pygame.font.SysFont(pygame.font.get_default_font(), 40)

	message_surface = None
	
	if player.player is None:
		message_surface = ui_font.render('.__. GAME OVER .__.', False, 'white')
	
	elif next_wave_cooldown > 0:
		# Countdown zeigen
		message_surface = ui_font.render(f'WAVE {current_wave_number} STARTS IN {next_wave_cooldown // 50 + 1}', False, 'white')
	
	if paused:
		message_surface = ui_font.render('--- PAUSED ---', False, 'white')
	
	score_surface = ui_font.render(f'SCORE: {score}', False, 'white')
	wave_surface  = ui_font.render(f'WAVE:  {current_wave_number}', False, 'white')
	
	if message_surface is not None:
		pygame.Surface.blit(screen, message_surface, (settings.WIDTH // 2 - message_surface.get_width() // 2, settings.HEIGHT // 2 - message_surface.get_height() // 2))
	
	pygame.Surface.blit(screen, score_surface, (0, 0))
	pygame.Surface.blit(screen, wave_surface, (0, score_surface.get_height()))


