import pygame #  @UnusedImport
from pygame.locals import * # @UnusedWildImport
import constantes

#Creer une jauge horizontal avec le pourcentage affiché à sa droite
class Jauge(object):
    def __init__(self,percent,posX,posY):
        self.ratioAffichage = constantes.para["ratioAffichage"]
        self.posX = posX
        self.posY = posY
        self.percent = percent
        self.largeur = 300*self.ratioAffichage
        self.hauteur = 16*self.ratioAffichage
        self.rect = Rect(posX,posY-self.hauteur/2,self.largeur,self.hauteur)
        self.police = pygame.font.Font(constantes.gameFont, int(22*self.ratioAffichage))     
        self.majTexte(percent)
        
        
        xRemplissage = posX+percent*(self.largeur/100)
        self.pointsRemplissage = [[posX,posY-self.hauteur/2],
                                  [xRemplissage,posY-self.hauteur/2],
                                  [xRemplissage,posY+self.hauteur/2-1],
                                  [posX,posY+self.hauteur/2-1]] 
        
        self.click = False
        
    def afficher(self,fenetre,poscurseur):
        pygame.draw.polygon(fenetre,(255,255,255),self.pointsRemplissage)
        pygame.draw.rect(fenetre,(150,151,160),self.rect,2)
        fenetre.blit(self.texte,(self.posX+self.largeur+(10*self.ratioAffichage),self.posY-self.texte.get_height()/2))
        self.majPourcentage(poscurseur)
        
    def majPourcentage(self,poscurseur):
        curseurX = poscurseur[0]
        if self.click :
            if curseurX > self.posX+self.largeur :
                self.majPointsXRemplissage(self.posX+self.largeur)
            elif curseurX < self.posX :
                self.majPointsXRemplissage(self.posX)
            else :
                self.majPointsXRemplissage(curseurX)
        self.percent = int((self.pointsRemplissage[1][0]-self.posX)/(self.largeur/100))
        self.majTexte(self.percent)
        
    def isPreselec(self,mouse_pos):    
        if (self.rect.collidepoint(mouse_pos)) :
            return True
        else :
            return False
        
    def majTexte(self,percent):
        textePoucentage = "{0}%".format(percent)
        self.texte = self.police.render(textePoucentage, 1, (255,255,255))
        
    def majPointsXRemplissage(self,x):
        self.pointsRemplissage[1][0] = x
        self.pointsRemplissage[2][0] = x