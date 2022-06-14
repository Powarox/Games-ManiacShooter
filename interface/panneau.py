import pygame
from pygame.locals import * # @UnusedWildImport
import constantes


class Panneau(object):
    def __init__(self,fenetre,titre,largeur,hauteur):

        self.fenetre = fenetre
        #Titre
        self.police = pygame.font.Font(constantes.gameFont, int(35*constantes.para["ratioAffichage"])) 
        self.titre = self.police.render(titre, 1, (255,255,255))
        self.larg_texte = self.titre.get_width()
        self.long_texte = self.titre.get_height()
        
        self.centreX = constantes.para["largeur"]/2
        self.limiteXdroit = (constantes.para["largeur"] + largeur)/2
        self.limiteXgauche = (constantes.para["largeur"] - largeur)/2
        self.limiteYhaut = (constantes.para["hauteur"]-hauteur)/2
        self.limiteYbas = (constantes.para["hauteur"]+hauteur)/2

        self.pointsTitre = [(self.centreX-(self.larg_texte*0.7),self.limiteYhaut),
                       (self.centreX-self.larg_texte/2,self.limiteYhaut-(self.long_texte*0.75)), 
                       (self.centreX+self.larg_texte/2,self.limiteYhaut-(self.long_texte*0.75)),
                       (self.centreX+(self.larg_texte*0.7),self.limiteYhaut),
                       (self.centreX+self.larg_texte/2,(self.limiteYhaut+(self.long_texte*0.75))),
                       (self.centreX-self.larg_texte/2,(self.limiteYhaut+(self.long_texte*0.75)))]
        
        
        
        self.contour = [(self.pointsTitre[3]),
                        (self.limiteXdroit,self.limiteYhaut),
                        (self.limiteXdroit,self.limiteYbas),
                        (self.limiteXgauche,self.limiteYbas),
                        (self.limiteXgauche,self.limiteYhaut),
                        (self.pointsTitre[0])]
        
    def afficher(self):
        pygame.draw.polygon(self.fenetre,(255,255,255),self.pointsTitre,2)
        self.fenetre.blit(self.titre,(self.centreX-self.larg_texte/2,self.limiteYhaut-self.long_texte/2))
        pygame.draw.lines(self.fenetre,(255,255,255),False,self.contour,2)