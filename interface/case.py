import pygame #  @UnusedImport
from pygame.locals import * # @UnusedWildImport
import constantes


class Case(object):
    def __init__(self,texte,posX,posY,cocher):
        demi_cote = int((30*constantes.para["ratioAffichage"])/2) #longueur demi-coté du carré
        self.posX = posX
        self.posY = posY
        self.pointsCase = [(posX-demi_cote,posY-demi_cote),
                       (posX-demi_cote,posY+demi_cote),
                       (posX+demi_cote,posY+demi_cote),
                       (posX+demi_cote,posY-demi_cote)] 
        
        self.pointsValider = [(posX-demi_cote*0.5+1,posY-demi_cote*0.4-2),
                       (posX+demi_cote*0.2,posY+demi_cote*0.5-4),
                       (posX+demi_cote*1.4-2,posY-demi_cote*0.8-2),
                       (posX+demi_cote*1.4+1,posY-demi_cote*0.8+2),
                       (posX+demi_cote*0.2,posY+demi_cote*0.5+2),
                       (posX-demi_cote*0.5-2,posY-demi_cote*0.4+2)] 
        
        self.isValide = cocher
        
        self.police = pygame.font.Font(constantes.gameFont, int(22*constantes.para["ratioAffichage"]))     
        self.texte = self.police.render(texte, 1, (255,255,255))
        
        
    def afficher(self,fenetre):
        self.bords = pygame.draw.polygon(fenetre,(255,255,255),self.pointsCase,2)
        fenetre.blit(self.texte,(self.posX+(35*constantes.para["ratioAffichage"]),self.posY-self.texte.get_height()/2))
        if self.isValide :
            pygame.draw.polygon(fenetre,(28,175,40),self.pointsValider)
            pygame.draw.aalines(fenetre,(28,175,40),True,self.pointsValider)

    def isPreselec(self,mouse_pos):    
        if (self.bords.collidepoint(mouse_pos)) :
            return True
        else :
            return False
        
    def click(self):
        if self.isValide :
            self.isValide = 0
        else :
            self.isValide = 1