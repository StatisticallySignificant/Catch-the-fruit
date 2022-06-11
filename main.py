# But : touche enfoncée -> le panier se déplace
# Jeu se lance
# Avoir un panier et des fruits 
import pygame, random, Panier, Fruits
from pygame.locals import *
from Panier import Panier
from Fruits import Fruit, create_fruit

pygame.init()

# le jeu tourne
running = True
# pas encore perdu
lost = False

# Gérer affichage
screen_size = [900,600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Collect the fruits")

# Gérer un temps
clock = pygame.time.Clock()
second_clock = pygame.time.Clock()

score = 0
# On définit le nombre max de sprites en même temps
fruits_maximum_count = 10 # Renamed vars
fruits = []
# Your usage of a sprite Group + a list to have all 
# the fruits is a bit wanky but ok

# On gère les coordonnées du Panier
player_dimensions = (100,100)
# Renamed misleading vars, I thought it was going to be the current position
# of the player but you only use it for its spawn 
spawn_player_x = screen_size[0]*0.5
spawn_player_y = screen_size[1] - player_dimensions[1]*1.5
# spawn_coords = (screen_size[0]*0.5, screen_size[1] - dimensions[1]*1.5) -> Could have been even better 

# Créer Group de fruits (sprites)
fruits_group = pygame.sprite.Group()


# Gère affichage du score en permanence
def collected_fruits(screen,score) :
	font = pygame.font.SysFont(None, 35) 
	text = font.render("Score "+str(score), True, (255,255,255))
	screen.blit(text,(0,0))

# Affichage écran de fin 
def end_screen(screen,score):
	font = pygame.font.SysFont(None, 50) 
	text = font.render("GameOver, your score: "+str(score), True, (255,255,255),(0,0,0))
	screen.blit(text,(200,300))

# There was here a lot of functions designed to 
# instantiate a fruit and add it to a Group of sprites
# I moved the whole into Fruits.py and deleted the 
# little ones

# Teste si possible de créer un nv fruit
def enough_time(passed_time) :
	if passed_time > 1500 :
		print("enough", passed_time)
		return(True)
	else :
		return(False)



# Créer un panier
panier = Panier(spawn_player_x, spawn_player_y, 500, player_dimensions)
# On créé notre premier fruit
create_fruit(fruits_group, screen_size[0])
last_created = 0

while running :
	# Le temps entre chaque frame en secondes
	delta_time = clock.tick(30)* 10**-3
	delta_time2 = second_clock.tick()
	last_created += delta_time2

	# Chercher les évènements 
	for event in pygame.event.get():
		# Gérer la fermeture du jeu
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_BACKSPACE) :
			running = False
			break
		
		pressed = pygame.key.get_pressed()
		# Panier déplaçable que si pas perdu 
		if lost == False :
			if pressed[pygame.K_LEFT]:
				panier.direction[0] = -1
			elif pressed[pygame.K_RIGHT]:
				panier.direction[0] = 1
			else:
				panier.direction[0] = 0

	#		if pressed[pygame.K_UP]:
	#			panier.direction[1] = -1
	#		elif pressed[pygame.K_DOWN]:
	#			panier.direction[1] = 1
	#		else:
	#			panier.direction[1] = 0

	# On vide l'écran
	screen.fill((0,0,0))

	panier.move(delta_time)

	fruits = pygame.sprite.Group.sprites(fruits_group)

	# On crée le max de sprites autorisé
	if len(fruits) < fruits_maximum_count and lost == False and enough_time(last_created) :
		create_fruit(fruits_group, screen_size[0])
		last_created = 0
		fruits = pygame.sprite.Group.sprites(fruits_group)
		

	for i in range (len(fruits)):
		spritei = fruits[i]
		move_tom_x, move_tom_y = spritei.rect[0], spritei.rect[1]
	
		# On va détecter la collision : si le panier se fait toucher par la tomate
		# alors on arrête de faire bouger la tomate et on arrête de la dessiner

		if (not panier.rect.colliderect(spritei.rect)) and (move_tom_y < screen_size[1] - 51) and fruits_group.has(spritei):
			spritei.move(delta_time)
			spritei.draw(screen)
		elif panier.rect.colliderect(spritei.rect) and fruits_group.has(spritei) :
			score+=1
			spritei.remove(fruits_group)

		elif move_tom_y >= screen_size[1] - 51  and fruits_group.has(spritei) :
			print ("raté")
			lost = True
			break


	if not lost: # (better readability) 
		panier.draw(screen)
		collected_fruits(screen,score)
		pygame.display.flip()
	else :
		screen.fill((0,0,0))
		end_screen(screen, score)
		pygame.sprite.Group.empty(fruits_group)
		pygame.display.flip()

pygame.quit()