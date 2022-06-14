import pygame
import random
import math
from pygame.locals import *   #@UnusedWildImport
import constantes

class Ennemi(pygame.sprite.Sprite):
    def __init__(self,pos,typeEnnemi):
        pygame.sprite.Sprite.__init__(self)
        self.type = typeEnnemi
        img = pygame.image.load(constantes.image_ennemi.format(self.type)).convert_alpha()
        self.image = pygame.transform.scale(img,(int(img.get_rect().width*constantes.para["ratioAffichage"]),int(img.get_rect().height*constantes.para["ratioAffichage"])))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.life = 2
        self.delai_tir = random.randrange(-100,0)
        
    def update(self):
        if self.rect.top > 0 :
            self.delai_tir += 1

class TirEnnemi(pygame.sprite.Sprite):
    def __init__(self,posEnnemi,posJoueur):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(constantes.image_tir_ennemi).convert()
        self.rect = self.image.get_rect()
        self.rect.x = posEnnemi.centerx
        self.rect.y = posEnnemi.bottom
        self.vitesse = 6*constantes.para["ratioAffichage"]
        
        #vise le joueur
        x = posJoueur.centerx-posEnnemi.centerx
        y = posJoueur.centery-posEnnemi.centery
        distE_J = math.hypot(x,y)
        d = distE_J/self.vitesse
        self.trajH = x/d
        self.trajV = y/d
        
    def update(self):
        self.rect = self.rect.move(self.trajH,self.trajV)
        if (self.rect.top > constantes.para["hauteur"]) or (self.rect.left > constantes.para["largeur"]) or (self.rect.right < 0) :
            self.kill()


def placementEnnemi(nbEnnemi,typeEnnemi): #fonction qui gère le placement des ennemis d'une vague selon leurs nombres
    listePlacement = []        #renvoie une liste de tuile des coordonnées de chaque ennemi de la vague
    ze = (constantes.para["largeur"],constantes.para["hauteur"]*-1.2)
    if nbEnnemi == 1 : #Si 1 ennemi dans la vague
        listePlacement.append((ze[0]/2,ze[1]/2))
    if nbEnnemi == 2 : #Si 2 ennemi dans la vague
        listePlacement.append((ze[0]/3,ze[1]/2))
        listePlacement.append((2*(ze[0]/3),ze[1]/2))
    if nbEnnemi == 3 : #etc...
        listePlacement.append((ze[0]/3,ze[1]/3))
        listePlacement.append((ze[0]/2,ze[1]/6))
        listePlacement.append((2*(ze[0]/3),ze[1]/3))
    if nbEnnemi == 9 : #etc...
        n = 100
        for i in range(nbEnnemi) :
            listePlacement.append((n,ze[1]/3))
            n += 100
    return listePlacement  



