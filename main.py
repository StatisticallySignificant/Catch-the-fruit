# But : touche enfoncée -> le panier se déplace
# Jeu se lance
# Avoir un panier et des fruits 
import pygame, random, Panier, Fruits
from pygame.locals import *
from Panier import Panier
from Fruits import Fruits

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
maximum = 10 
mysprites = []


# On gère les coordonnées du Panier
dimensions = (100,100)
panier_x = screen_size[0]*0.5
panier_y = screen_size[1] - dimensions[1]*1.5

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

# Choix couleur ou image des fruits
def fruit_color():
	list_color = [1,(255,0,0),(0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (70,70,70), (255,255,255)]
	color_number = (random.randint(0,8))
	color = list_color[color_number]
	return (color)

# Choisir vitesse initiale aléatoirement
def fruit_speed():
	speed = 90 #random.randint(90,250)
	return (speed)

# Gérer coordonnées initiales fruits
def coordinate_fruit(screen_size):
	x = random.randint(0, screen_size[0]-50) 
	# - la dimension x du fruit car coordonées en haut à gauche 
	y = -10
	return((x,y))

# Créer une instance fruit qui hérite de Fruits
# Ajouter le nouveau sprite au Group de sprite
def create_fruit(fruits_group):
	newfruit = Fruits(fruits_group, coordinate_fruit(screen_size),fruit_speed(), (50,50), fruit_color())
	fruits_group.add(newfruit)


# Teste si possible de créer un nv fruit
def enough_time(passed_time) :
	if passed_time > 1500 :
		return(True)
	else :
		return(False)



# Créer un panier
panier = Panier(panier_x, panier_y, 500, dimensions)
# On créé notre premier fruit
create_fruit(fruits_group)
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
			if pressed[pygame.K_LEFT] : # and not (panier.rect.collidepoint(0,500)):
				panier.direction[0] = -1
			elif pressed[pygame.K_RIGHT]: # and not (panier.rect.collidepoint(900,500)):
				panier.direction[0] = 1
			#elif panier.rect[0]<=0 :
			#	panier.direction[0] = 0
			#	panier.rect[0]=0
			else:
				panier.direction[0] = 0
	#		panier.rect.clamp_ip(screen)

	#		if pressed[pygame.K_UP]:
	#			panier.direction[1] = -1
	#		elif pressed[pygame.K_DOWN]:
	#			panier.direction[1] = 1
	#		else:
	#			panier.direction[1] = 0

	# On vide l'écran
	screen.fill((0,0,0))

	panier.move(delta_time)

	mysprites = pygame.sprite.Group.sprites(fruits_group)

	# On crée le max de sprites autorisé
	if len(mysprites) < maximum and lost == False and enough_time(last_created) :
		create_fruit(fruits_group)
		last_created = 0
		mysprites = pygame.sprite.Group.sprites(fruits_group)
		

	for i in range (len(mysprites)):
		spritei = mysprites[i]
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
			lost = True
			break


	if lost == False :
		panier.draw(screen)
		collected_fruits(screen,score)
		pygame.display.flip()
	else :
		screen.fill((0,0,0))
		end_screen(screen, score)
		pygame.sprite.Group.empty(fruits_group)
		pygame.display.flip()

pygame.quit()