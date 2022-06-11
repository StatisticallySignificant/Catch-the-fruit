# On veut que des fruits soient générés aléatoirement en haut d'une map
# S'ils tombent dans le panier, ils disparaissent et on ajoute un point
# S'ils touchent le sol, ils disparaissent
# Est-ce qu'ils ont tous la même orientation ?
# Avoir un collider pour détecter le panier
import random, pygame
from pygame.locals import *

class Fruits(pygame.sprite.Sprite):
	def __init__(self, fruits_group, coordinate, speed, dimensions, color):
		pygame.sprite.Sprite.__init__(self)
		# les fruits tombent -> direction en ligne droite
		self.direction = [0,1]
		self.speed = speed
		x = coordinate[0]
		y = coordinate[1]
		self.x = coordinate[0]
		self.y = coordinate[1]
		if color == 1 :
			self.surface = pygame.image.load("Catch_Fruits\pred_apple.png")
			self.surface = pygame.transform.scale(self.surface, dimensions)

		else :
			self.surface = pygame.Surface(dimensions)
		# Mon rect, c'est une surface rectangulaire avec 2 coordonnées
		# Elle pourrait en avoir 4 : x,y,hauteur,largeur
		self.rect = self.surface.get_rect(x=x,y=y)
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
