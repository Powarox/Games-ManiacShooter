import pygame #  @UnusedImport
from pygame.locals import * # @UnusedWildImport
import constantes


class ChoixDeroulant(object):
    def __init__(self,tabElement,posX,posY,valDefaut):
        self.ratioAffichage = constantes.para["ratioAffichage"]
        self.posX = posX
        self.posY = posY
        self.police = pygame.font.Font(constantes.gameFont, int(22*self.ratioAffichage))     
        self.texteDefaut = self.police.render(valDefaut, 1, (255,255,255))
        self.tabTexte = []
        self.tabZoneChoix = []
        self.largeur = 300*self.ratioAffichage
        self.hauteur_texte = self.texteDefaut.get_height()
        self.demi_hauteur = self.hauteur_texte*0.7
        self.isActive = False
        self.choix = -1

        y = posY
        for element in tabElement :
            self.tabTexte.append(self.police.render(element, 1, (255,255,255)))
            self.tabZoneChoix.append(Rect(posX,
                                           y+self.demi_hauteur,
                                           posX+self.largeur-posX,
                                           self.demi_hauteur*2.5))
                            
            y += self.demi_hauteur*2.5
        
        self.pointsContour = [(posX,posY-self.demi_hauteur),
                       (posX,posY+self.demi_hauteur),
                       (posX+self.largeur,posY+self.demi_hauteur),
                       (posX+self.largeur,posY-self.demi_hauteur)]
         
        self.pointsZoneSelec = [(posX,posY+self.demi_hauteur),
                       (posX,posY+self.demi_hauteur*2*(len(tabElement)+1)),
                       (posX+self.largeur,posY+self.demi_hauteur*2*(len(tabElement)+1)),
                       (posX+self.largeur,posY+self.demi_hauteur)]
        
        
        self.btnDefilement = [(posX+self.largeur+2*self.demi_hauteur,posY-self.demi_hauteur),
                       (posX+self.largeur+2*self.demi_hauteur,posY+self.demi_hauteur),
                       (posX+self.largeur,posY+self.demi_hauteur),
                       (posX+self.largeur,posY-self.demi_hauteur)]
        
        self.pointsFleche = [(self.btnDefilement[2][0]+self.demi_hauteur*0.6,posY-self.demi_hauteur*0.4),
                       (self.btnDefilement[2][0]+self.demi_hauteur*1.4,posY-self.demi_hauteur*0.4),
                       (self.btnDefilement[2][0]+self.demi_hauteur,posY+self.demi_hauteur*0.4)]
        
        
        self.pointsActiveFleche = [(self.btnDefilement[2][0]+self.demi_hauteur*0.6,posY+self.demi_hauteur*0.4),
                       (self.btnDefilement[2][0]+self.demi_hauteur*1.4,posY+self.demi_hauteur*0.4),
                       (self.btnDefilement[2][0]+self.demi_hauteur,posY-self.demi_hauteur*0.4)]
        
        
    def afficher(self,fenetre):
        self.bords = pygame.draw.polygon(fenetre,(255,255,255),self.pointsContour,2)
        self.btn = pygame.draw.polygon(fenetre,(255,255,255),self.btnDefilement,2)
        fenetre.blit(self.texteDefaut,(self.posX+(10*self.ratioAffichage),self.posY-self.hauteur_texte/2))
        if self.isActive :
            self.fleche = pygame.draw.polygon(fenetre,(255,255,255),self.pointsActiveFleche)
            self.aaFleche = pygame.draw.aalines(fenetre,(255,255,255),True,self.pointsActiveFleche)
            y = self.pointsZoneSelec[0][1]+self.hauteur_texte/2
            self.bordSelect = pygame.draw.polygon(fenetre,(255,255,255),self.pointsZoneSelec,2)
            for texte in self.tabTexte :
                fenetre.blit(texte,(self.posX+(10*self.ratioAffichage),y))
                y += self.demi_hauteur*2
        else :
            self.fleche = pygame.draw.polygon(fenetre,(255,255,255),self.pointsFleche)
            self.aaFleche = pygame.draw.aalines(fenetre,(255,255,255),True,self.pointsFleche)
                
    def isBtnPreselec(self,mouse_pos):    
        if (self.bords.collidepoint(mouse_pos) or self.btn.collidepoint(mouse_pos)) :
            return True
        else :
            return False
        
    def clickBtn(self):
        if self.isActive :
            self.isActive = False
        else :
            self.isActive = True
            
    def choixPreselec(self,mouse_pos):
        for i in range(self.tabZoneChoix.__len__()) :    
            if (self.tabZoneChoix[i].collidepoint(mouse_pos)) :
                self.preselecChoix = i
                return True
        return False
    
    def clickChoix(self):
        self.texteDefaut = self.police.render(constantes.tabDimension[self.preselecChoix], 1, (255,255,255))
        self.choix = self.preselecChoix
