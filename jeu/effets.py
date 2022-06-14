import pygame
from pygame.locals import *   #@UnusedWildImport
from constantes import *  #@UnusedWildImport

#Initialisation du son

sonImpact = pygame.mixer.Sound(son_impact)
sonExplosion = pygame.mixer.Sound(son_explosion)


class Impact (pygame.sprite.Sprite):

	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		sonImpact.play()
		self.imgNum = 0
		self.image = pygame.image.load(image_impact.format(self.imgNum)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = pos
		
	def update(self, *args):
		pygame.sprite.Sprite.update(self, *args)
		self.imgNum += 1
		self.image = pygame.image.load(image_impact.format(self.imgNum)).convert_alpha()
		if self.imgNum == 9 :
			self.kill() 
		
		
class Explosion (pygame.sprite.Sprite):
	def __init__(self,pos):
		pygame.sprite.Sprite.__init__(self)
		sonExplosion.play()
		self.imgNum = 1
		self.image = pygame.image.load(image_explosion.format(self.imgNum)).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.center = pos
		
	def update(self, *args):
		pygame.sprite.Sprite.update(self, *args)
		self.imgNum += 1
		if self.imgNum <= 18 :
			self.image = pygame.image.load(image_explosion.format(self.imgNum)).convert_alpha()
		else :
			self.kill()	
		
		
		
		
		
			
	