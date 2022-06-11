 # On veut qu'un panier puisse collecter les fruits
 # On peut déplacer le panier de gauche à droite et de haut en bas
 # Le fruit et le panier doivent avoir un collider
import pygame

# Panier and Fruit classes both has:
# a rect, an image, a position, a direction, a speed, a draw function and a move function
# Maybe they could have been the same class or they could have inherited from the same class
# so we don't write two times the same code

class Panier:
	def __init__(self, x, y, speed, dimensions, direction=[0,0]):
		self.image = pygame.image.load("panier_fondnoir_rogne.png") # It was working for you ? It couldn't find the png file for me
		self.image = pygame.transform.scale(self.image, dimensions)
		# la direction dépend de la touche appuyée par le joueur
		self.direction = direction
		self.speed = speed
		self.rect = self.image.get_rect(x=x,y=y)

	def draw(self,screen):
		screen.blit(self.image, self.rect)

	def move(self,delta_time):
		# normalize vector
		self.rect.move_ip(self.direction[0] * self.speed*delta_time, self.direction[1] * self.speed*delta_time)
	