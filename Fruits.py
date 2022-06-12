# Goal of this file : Fruits appear at random place on top of the screen
# Est-ce qu'ils ont tous la même orientation ?
# They have a surface to be detected by the basket
import random, pygame
from pygame.locals import *

class Fruit(pygame.sprite.Sprite):
	current_speed = 120
	@staticmethod
	def increase_speed_by(add):
		Fruit.current_speed += add

	def __init__(self, fruits_group, coordinate, dimensions, color):
		pygame.sprite.Sprite.__init__(self, [fruits_group])
		# Fruits are falling vertically
		self.direction = [0,1]
		# x and y (not self.x and self.y) are a temporary copy of self.x and self.y
		# (because the variable is created inside a function, it will "die" at the end of it)

		self.x, self.y = coordinate

		if color == 1 :
			self.surface = pygame.image.load("pred_apple.png")
			self.surface = pygame.transform.scale(self.surface, dimensions)
		else :
			self.surface = pygame.Surface(dimensions)
		# Rect is a rectangular surface with 2 coordinates
		# It could have 4 : x,y,heigh,width
		self.rect = self.surface.get_rect(x=self.x,y=self.y)
		if color != 1:
			self.surface.fill(color)

	# Display fruit
	def draw(self, screen):
		screen.blit(self.surface, self.rect)

	def move(self, delta_time):
		self.rect.move_ip(self.direction[0] * Fruit.current_speed * delta_time, self.direction[1] * Fruit.current_speed *delta_time)

# This function is outside of the class fruit (we import it)
# but we could have put it inside (and static) if we want

def create_fruit(fruits_group, screen_width):
	# We randomly choose a color (or an image) and the coordinates 
	list_color = [1, (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (70,70,70), (255,255,255)]
	color = list_color[random.randint(0, len(list_color)-1)]
	coordinate = (random.randint(0, screen_width-50), -10)
	dimensions = (50,50)
	return Fruit(fruits_group, coordinate, dimensions, color)

# Here, we also could have done :
# def create_fruit(fruits_group, screen_width):
# 	all_colors = [1,(255,0,0),(0,255,0), (0,0,255), (255,255,0), (0,255,255), (255,0,255), (70,70,70), (255,255,255)]
# 	return Fruit(
# 		fruits_group, 
# 		coordinate= (random.randint(0, screen_width-50), -10), 
# 		speed=60, 
# 		dimensions=(50,50), 
# 		color=all_colors[random.randint(0, len(all_colors)-1)]
# 	)

