 # On veut qu'un panier puisse collecter les fruits
 # On peut déplacer le panier de gauche à droite et de haut en bas
 # Le fruit et le panier doivent avoir un collider
import pygame

class Panier:
	def __init__(self, x, y, speed, dimensions, direction=[0,0]):
		self.image = pygame.image.load("Catch_Fruits\panier_fondnoir_rogne.png")
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
	