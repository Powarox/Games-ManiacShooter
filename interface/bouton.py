import pygame
import constantes

pygame.mixer.pre_init(44100,-16,2,2048)
pygame.mixer.init(44100, -16, 2, 2048)

sonClick = pygame.mixer.Sound(constantes.son_btnClick)
sonPreselec = pygame.mixer.Sound(constantes.son_btnPreselec)
                                                                    

class Bouton(object):
    
    def __init__(self,fenetre,texte,position): #la position donnée en paramètre est la position du centre du bouton
        self.fenetre = fenetre
        self.police = pygame.font.Font(constantes.gameFont, int(30*constantes.para["ratioAffichage"]))     
        self.texte = self.police.render(texte, 1, (255,255,255))
        self.larg_texte = self.texte.get_width()
        self.long_texte = self.texte.get_height()
        self.posX = position[0]
        self.posY = position[1]
        self.largeur = constantes.para["largeur"]/3
        self.longueur = constantes.para["hauteur"]/8
        self.isPreSoundPlayed = False
        self.points = [(self.posX-self.largeur/2,self.posY-self.longueur/2), #Points du rectangle qui entoure le bouton
                        (self.posX-self.largeur/2,self.posY+self.longueur/2),
                        (self.posX+self.largeur/2,self.posY+self.longueur/2),
                        (self.posX+self.largeur/2,self.posY-self.longueur/2)]
        self.preselec_points = [(self.posX-self.largeur/2-10,self.posY-self.longueur/2-10),
                        (self.posX-self.largeur/2-10,self.posY+self.longueur/2+10),
                        (self.posX+self.largeur/2+10,self.posY+self.longueur/2+10),
                        (self.posX+self.largeur/2+10,self.posY-self.longueur/2-10)]
        
        
    def afficher(self):
        self.bords = pygame.draw.lines(self.fenetre,(255,255,255),True,self.points,3)
        self.fenetre.blit(self.texte,(self.posX-self.larg_texte/2,self.posY-self.long_texte/2))
        
    def isPreselec(self,mouse_pos):    
        if (self.bords.collidepoint(mouse_pos)) :
            self.preselec_bords = pygame.draw.lines(self.fenetre,(255,255,255),True,self.preselec_points,3)
            if self.isPreSoundPlayed == False and constantes.para["audio"] :
                self.isPreSoundPlayed = True
                sonPreselec.set_volume(constantes.para["ratioVolInterface"])
                sonPreselec.play()
            return True
        else :
            self.isPreSoundPlayed = False
            return False
        
def playClickSound() :
    if constantes.para["audio"] :
        sonClick.set_volume(constantes.para["ratioVolInterface"])
        sonClick.play()
    