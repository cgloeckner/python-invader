import pygame

import settings
import game_object
import player
import enemy
import bullet
import effect
import powerup
import wave


def start_game():
	pygame.init()

	screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
	clock = pygame.time.Clock()
	
	pygame.event.set_grab(True)
	pygame.mouse.set_visible(False)
	
	wave.restart()
	
	running = True
	delta_time = 0

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

		has_focus = pygame.mouse.get_focused()

		if not has_focus:
			wave.paused = True
		elif wave.paused:
			wave.paused = False

		if not wave.paused:
			# Objekte aktualisieren
			player.update()
			game_object.update_all()
			enemy.update_all()
			bullet.update_all()
			effect.update_all()
			cleanup()
			wave.update()
			
		# Szene zeichnen
		screen.fill('black')
		game_object.draw_all(screen, False)
		powerup.draw_all(screen)
		effect.draw_all(screen)
		wave.draw(screen)
		
		pygame.display.update()
		
		# FPS begrenzen
		clock.tick(60)

	pygame.quit()


def cleanup():
	for data in game_object.destroyed:
		game_object.all_objects.remove(data)
		
		if data in enemy.all_enemies:
			enemy.all_enemies.remove(data)
			enemy.on_destroy(data)
		
		elif data == player.player:
			player.player = None
	
	game_object.destroyed = []


if __name__ == '__main__':
	start_game()

