# The game is on
# Goal of this file : handle events (play, move, retry, quit), moment of creation of the fruit, score
from time import time
import pygame
from pygame.locals import *
from Panier import Panier
from Fruits import Fruit, create_fruit

pygame.init()

# Game is running
running = True
# Player did neither lost or play
lost = False
last_best_score = 0
game_played = 0
score = 0

# Handle screen and display
screen_size = [900,600]
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Collect the fruits")

# Handle time
# The clock is used to :
# - know when last fruit was created
# - increase game difficulty over time
# - move player at the same speed event if FPS changes
clock = pygame.time.Clock()

# Initialize fruit list
# Usage of a sprite Group + a list to have all 
# the fruits is probably unefficient
fruits = []

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
def end_screen(screen, game_played, last_best_score,score, i): 
	# Text to explain player he has lost
	font_gameover = pygame.font.SysFont(None, 50) 
	text_gameover = font_gameover.render("GameOver, your score: "+str(score), True, (255,255,255),(0,0,0))
	# If it is the first frame player goes in end_screen of this atempt :
	if i :
		font_bestscore = pygame.font.SysFont(None,30)
		if game_played==1 : # If it is the first game, there is no best score
			text_best_score = font_bestscore.render("First best score",True,(255,255,255))
			last_best_score = score

		elif last_best_score < score : # If player did better, it is a new best score
			text_best_score = font_bestscore.render("New best score, last best score = "+str(last_best_score),True,(255,255,255))
			last_best_score = score

		elif last_best_score > score : # If player didn't do better, show last best score
			text_best_score = font_bestscore.render("Best Score ="+str(last_best_score),True,(255,255,255))

		else : # if player did same score as best score, tell player
			text_best_score = font_bestscore.render ("Same best score ", True, (255,255,255))
		
		# Display 
		screen.blit(text_gameover,(200,250))
		screen.blit(text_best_score,(220,350))
		text_retry = font_bestscore.render("Press P to retry", True, (255,0,10))
		screen.blit(text_retry, (220,450))
		pygame.display.flip()
		i = False

	return last_best_score, game_played, i

# Handle speed
time_in_game = 0
last_speed_increase = 0 # last time the player speed did increase
time_before_spawn = 2000 # in millisecond
last_spawtime_increase = 0 # last time the time before 2 fruits can spawn increased

def handle_speed_and_spawntime():
	global time_in_game, last_speed_increase, last_spawtime_increase, time_before_spawn
	# If it has been more than 2seconds that the fruits speed increased, increase fruits speed
	if time_in_game - last_speed_increase >=2 :
		Fruit.increase_speed_by(2)
		last_speed_increase = time_in_game
	# If it has been more than 8 seconds that the fruits spawn delay increased, increase it
	if time_in_game-last_spawtime_increase >= 6:
		time_before_spawn-=100
		last_spawtime_increase = time_in_game

# Create the basket
panier = Panier(spawn_player_x, spawn_player_y, 500, player_dimensions)
# Create the first fruit and initialising time between each fruit
create_fruit(fruits_group, screen_size[0])
last_created = 0

while running :
	# time bewteen two frames
	delta_time = clock.tick(30)* 10**-3
	last_created += delta_time* 10**3
	time_in_game +=delta_time

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
		if lost :
			# The player can retry only if he has already lost
			if pressed[pygame.K_p]:
				lost = False
				screen.fill((0,0,0))
				score = 0
				fruits =[]
				time_in_game = 0
				last_speed_increase = 0
				time_before_spawn = 2000
				last_spawtime_increase = 0	
				panier = Panier(spawn_player_x, spawn_player_y, 500, player_dimensions)
				create_fruit(fruits_group, screen_size[0])
				last_created = 0

	# Clear screen
	screen.fill((0,0,0))

	panier.move(delta_time)

	fruits = pygame.sprite.Group.sprites(fruits_group)

	# Create fruit if conditions are okay
	if not lost and last_created > time_before_spawn :
		create_fruit(fruits_group, screen_size[0])
		last_created = 0
		fruits = pygame.sprite.Group.sprites(fruits_group)
		
	# Handle each fruit move and event
	for spritei in fruits:
		# If it is still falling, it keeps falling and is on screen
		if (not panier.rect.colliderect(spritei.rect)) and (spritei.rect[1] < screen_size[1] - 51) and fruits_group.has(spritei):
			spritei.move(delta_time)
			spritei.draw(screen)
		# If the basket touchs the fruit, the score rise 
		# and the fruit disapear
		elif panier.rect.colliderect(spritei.rect) and fruits_group.has(spritei) :
			score+=1
			spritei.remove(fruits_group)
			handle_speed_and_spawntime()
		# If the fruit touchs the ground, the player loose (only once per game)
		elif spritei.rect[1] >= screen_size[1] - 51  and fruits_group.has(spritei) :
			lost = True
			game_played+=1
			i=True
			break

	if not lost: 
		panier.draw(screen)
		collected_fruits(screen,score)
		pygame.display.flip()
	# If the game is lost, show player end screen
	else :
		screen.fill((0,0,0))
		last_best_score, game_played, i = end_screen(screen, game_played, last_best_score, score, i)
		pygame.sprite.Group.empty(fruits_group)
		

pygame.quit()