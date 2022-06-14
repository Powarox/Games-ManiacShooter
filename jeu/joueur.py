import pygame
from pygame.locals import *
import constantes

sonTir = pygame.mixer.Sound(constantes.son_tir)

class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(constantes.image_perso).convert_alpha()
        self.image = pygame.transform.scale(img,(int(img.get_rect().width*constantes.para["ratioAffichage"]),int(img.get_rect().height*constantes.para["ratioAffichage"])))
        self.rect = self.image.get_rect()
        self.rect.x = (constantes.para["largeur"]-self.rect.width)/2
        self.rect.y = (constantes.para["hauteur"]*0.97)-self.rect.height
        self.delai_tir = 0
        self.vie = 3
        self.vitesse = 5*constantes.para["ratioAffichage"]
        self.score = 0
        self.grp_tir = pygame.sprite.Group() 

    def controleJoueur(self): #fonction qui gère les actions du joueur selon les touches préssés
        v = 0
        h = 0
        k = pygame.key.get_pressed(); #Récuperation de toute les touches préssés
        if k[K_s] and (self.rect.bottom < constantes.para["hauteur"]):    #Si "flèche bas"             @UndefinedVariable
            v += self.vitesse
        if k[K_z] and (self.rect.top > 0):    #Si "flèche haut"                         @UndefinedVariable
            v -= self.vitesse
        if k[K_q] and (self.rect.left > 0):    #Si "flèche gauche"                     @UndefinedVariable
            h -= self.vitesse
        if k[K_d] and (self.rect.right < constantes.para["largeur"]):    #Si "flèche droite"             @UndefinedVariable
            h += self.vitesse
        self.rect = self.rect.move(h,v)
        if k[K_SPACE] and self.delai_tir >= 30 :                                                     #@UndefinedVariable
            tir = Tir(self.rect)
            self.grp_tir.add(tir)
            self.delai_tir = 0
        else :
            self.delai_tir += 1 


class Tir(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        sonTir.play()
        self.image = pygame.image.load(constantes.image_tir).convert()
        self.rect = self.image.get_rect()
        self.rect.x = position.centerx
        self.rect.y = position.top
    
    def update(self):
        self.rect = self.rect.move(0,-25*constantes.para["ratioAffichage"])
        if (self.rect.top < 0) :
            self.kill()
        




