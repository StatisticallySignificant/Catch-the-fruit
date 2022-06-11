# The game is on
# Goal of this file : handle moves and events
import pygame, Panier, Fruits
from pygame.locals import *
from Panier import Panier
from Fruits import Fruit, create_fruit

pygame.init()

# Game is running
running = True
# Player has not lost
lost = False

# Handle screen and display
screen_size = [900,600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Collect the fruits")

# Handle time
clock = pygame.time.Clock()
second_clock = pygame.time.Clock()

score = 0
fruits = []
# Usage of a sprite Group + a list to have all 
# the fruits is probably unefficient

# Handling basket dimensions and initial coordinates
player_dimensions = (100,100) 
spawn_player_x = screen_size[0]*0.5
spawn_player_y = screen_size[1] - player_dimensions[1]*1.5
# spawn_coords = (screen_size[0]*0.5, screen_size[1] - dimensions[1]*1.5) -> Could have been even better 

# Create Group of fruits (sprites)
fruits_group = pygame.sprite.Group()

# Handling score display
def collected_fruits(screen,score) :
	font = pygame.font.SysFont(None, 35) 
	text = font.render("Score "+str(score), True, (255,255,255))
	screen.blit(text,(0,0))

# Handling last screen display 
def end_screen(screen,score):
	font = pygame.font.SysFont(None, 50) 
	text = font.render("GameOver, your score: "+str(score), True, (255,255,255),(0,0,0))
	screen.blit(text,(200,300))

# Create the basket
panier = Panier(spawn_player_x, spawn_player_y, 500, player_dimensions)
# Create the first fruit and initialising time between each fruit
create_fruit(fruits_group, screen_size[0])
last_created = 0

while running :
	# time bewteen two frames
	delta_time = clock.tick(30)* 10**-3
	delta_time2 = second_clock.tick()
	last_created += delta_time2

	# Handle events 
	for event in pygame.event.get():
		# quit events
		if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_BACKSPACE) :
			running = False
			break
		
		pressed = pygame.key.get_pressed()
		# The player can move only if he has not lost 
		if not lost :
			# Handle horizontals move of the basket
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

	# Clear screen
	screen.fill((0,0,0))

	panier.move(delta_time)

	fruits = pygame.sprite.Group.sprites(fruits_group)

	# Create fruit if necessary
	if not lost and last_created>1500 :
		create_fruit(fruits_group, screen_size[0])
		last_created = 0
		fruits = pygame.sprite.Group.sprites(fruits_group)
		
	# Handle fruit move and event
	for i in range (len(fruits)):
		spritei = fruits[i]
		move_tom_x, move_tom_y = spritei.rect[0], spritei.rect[1]
	
		# If it is still falling, it keeps falling and is on screen
		if (not panier.rect.colliderect(spritei.rect)) and (move_tom_y < screen_size[1] - 51) and fruits_group.has(spritei):
			spritei.move(delta_time)
			spritei.draw(screen)
		# If the basket touchs the fruit, the score rise 
		# and the fruit disapear
		elif panier.rect.colliderect(spritei.rect) and fruits_group.has(spritei) :
			score+=1
			spritei.remove(fruits_group)

		# If the fruit touchs the ground, the player loose
		elif move_tom_y >= screen_size[1] - 51  and fruits_group.has(spritei) :
			lost = True
			break

	if not lost: 
		panier.draw(screen)
		collected_fruits(screen,score)
		pygame.display.flip()
	else :
		screen.fill((0,0,0))
		end_screen(screen, score)
		pygame.sprite.Group.empty(fruits_group)
		pygame.display.flip()

pygame.quit()