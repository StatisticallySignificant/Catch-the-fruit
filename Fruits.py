# On veut que des fruits soient générés aléatoirement en haut d'une map
# S'ils tombent dans le panier, ils disparaissent et on ajoute un point
# S'ils touchent le sol, ils disparaissent
# Est-ce qu'ils ont tous la même orientation ?
# Avoir un collider pour détecter le panier
import random, pygame
from pygame.locals import *

# Renamed the class because an instance of this class represent
# a single fruit and not a group of fruits
# before: Fruits, now: Fruit
class Fruit(pygame.sprite.Sprite):
	def __init__(self, fruits_group, coordinate, speed, dimensions, color):
		# You weren't using the fruits_group var
		# We can see by pressing F12 after clicking on
		# the pygame.sprite.Sprite.__init__ that the function
		# asks for a Group, and add the new sprite to the group
		# automatically (what you were doing manually in your
		# "create_fruit" function)
		pygame.sprite.Sprite.__init__(self, [fruits_group])

		# les fruits tombent -> direction en ligne droite
		self.direction = [0,1]
		self.speed = speed

		# x and y (not self.x and self.y) are a temporary copy of self.x and self.y
		# (because the variable is created inside a function, it will "die" at the end of it)
		# so they are useless ^^
		#x = coordinate[0]
		#y = coordinate[1]

		self.x = coordinate[0]
		self.y = coordinate[1]

		if color == 1 :
			self.surface = pygame.image.load("pred_apple.png") # It was working for you ? It couldn't find the png file for me
			self.surface = pygame.transform.scale(self.surface, dimensions)
		else :
			self.surface = pygame.Surface(dimensions)
		# Mon rect, c'est une surface rectangulaire avec 2 coordonnées
		# Elle pourrait en avoir 4 : x,y,hauteur,largeur
		self.rect = self.surface.get_rect(x=self.x,y=self.y)
		if color != 1:
			self.surface.fill(color)
		# J'ajoute mon fruit à la liste de fruits
		# Enfin non, finalement c'est fait ailleurs

	# On va devoir générer des fruits
	# Pour le moment on peut les représenter par des rectangles
	def draw(self, screen):
		screen.blit(self.surface, self.rect)


	def move(self, delta_time):
		self.rect.move_ip(self.direction[0] * self.speed*delta_time, self.direction[1] * self.speed*delta_time)

# This function is outside of the class fruit
# but we could have put it inside (and static) if we want
# The function is long to read but only because of all the 
# unecessary commentaries
def create_fruit(fruits_group, screen_width):
	# Color
	list_color = [1,(255,0,0),(0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (70,70,70), (255,255,255)]
	# color_number = (random.randint(0,8))
	# color = list_color[color_number]
		# Faster like this and independant of the size of the list
	color = list_color[random.randint(0, len(list_color)-1)]

	# Coordinate
	# x = random.randint(0, screen_size[0]-50) 
	# # - la dimension x du fruit car coordonées en haut à gauche 
	# y = -10
	# return ((x, y))
		# Less line -> faster to read (not always true in general but ^^)
	coords = (random.randint(0, screen_width-50), -10)

	# Speed
	speed = 90
	# Dimensions
	dimensions = (50,50)

	return Fruit(fruits_group, coords, speed, dimensions, color)

# Just for demonstration, here what we also could have done for 
# the same function 
# def create_fruit(fruits_group, screen_width):
# 	all_colors = [1,(255,0,0),(0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (70,70,70), (255,255,255)]
# 	return Fruit(
# 		fruits_group, 
# 		coordinate= (random.randint(0, screen_width-50), -10), 
# 		speed=60, 
# 		dimensions=(50,50), 
# 		color=all_colors[random.randint(0, len(all_colors)-1)]
# 	)

