import pygame
import sys
from pygame.locals import *
import constantes
from interface.bouton import *
from interface.score import *
from interface import bouton

class Menu(object):
	
	def __init__(self, screen):
		hauteur = constantes.para["hauteur"]
		largeur = constantes.para["largeur"]
		bg = pygame.image.load(constantes.backgroundMenu).convert()
		self.background = pygame.transform.scale(bg,(largeur,hauteur))
		self.fenetre = screen
		
		#Informe quel choix a été effectué
		self.start_selected = False
		self.settings_selected = False
		self.score_selected = False
		
		#Initialisation des boutons
		self.list_button = []
		b_jouer = Bouton(self.fenetre,"Jouer",(largeur/2,2*hauteur/10))
		b_scores = Bouton(self.fenetre,"Scores",(largeur/2,4*hauteur/10))
		b_param = Bouton(self.fenetre,"Paramètre",(largeur/2,6*hauteur/10))
		b_quitter = Bouton(self.fenetre,"Quitter",(largeur/2,8*hauteur/10))
		self.list_button.append(b_jouer)
		self.list_button.append(b_scores)
		self.list_button.append(b_param)
		self.list_button.append(b_quitter)
		self.preselec_button = -1

	def run(self):
		mainloop = True
		while mainloop:
			for event in pygame.event.get():   
				if event.type == QUIT:			   #@UndefinedVariable
					sys.exit()
				if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.preselec_button != -1 : #@UndefinedVariable
					bouton.playClickSound()
					if self.preselec_button == 0 :
						self.start_selected = True
					if self.preselec_button == 1 :
						self.score_selected = True
					if self.preselec_button == 2 :
						self.settings_selected = True
					if self.preselec_button == 3 :
						sys.exit()
					mainloop = False
					
			self.fenetre.blit(self.background,(0,0))		
			
			cursor_pos = pygame.mouse.get_pos()
			self.preselec_button = -1
			for i in range(self.list_button.__len__()) :	
				self.list_button[i].afficher()
				isPreselec = self.list_button[i].isPreselec(cursor_pos)
				if isPreselec :
					
					self.preselec_button = i	
				
			pygame.display.flip()


	





