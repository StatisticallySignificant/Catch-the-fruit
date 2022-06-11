 # We want a basket to collect the fruit
 # The player can move the basket
 # The basket has a collider
import pygame

class Panier:
	def __init__(self, x, y, speed, dimensions, direction=[0,0]):
		self.image = pygame.image.load("panier_fondnoir_rogne.png") 
		self.image = pygame.transform.scale(self.image, dimensions)
		# The initial direction is (0,0)
		self.direction = direction
		self.speed = speed
		self.rect = self.image.get_rect(x=x,y=y)

	def draw(self,screen):
		screen.blit(self.image, self.rect)

	def move(self,delta_time):
		# We don't normalize vector because it can move only honrizontally
		self.rect.move_ip(self.direction[0] * self.speed*delta_time, self.direction[1] * self.speed*delta_time)
	