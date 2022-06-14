import pygame #  @UnusedImport
from pygame.locals import * # @UnusedWildImport
from interface.bouton import Bouton
import constantes
import sys
from interface.tableauScore import TableauScore
from interface import bouton
from interface.panneau import Panneau

class Score(object):
    def __init__(self,screen):
        self.fenetre = screen
        largeurFenetre = constantes.para["largeur"]
        hauteurFenetre = constantes.para["hauteur"]
        bg = pygame.image.load(constantes.backgroundMenu).convert()
        self.background = pygame.transform.scale(bg,(largeurFenetre,hauteurFenetre))
        
        #Bouton retour
        self.btn_retour = Bouton(self.fenetre,"Retour",(largeurFenetre*0.5,hauteurFenetre*0.8))
        self.preselec_btnRetour = False
        
        #Panneau   
        self.panneau = Panneau(self.fenetre,"Scores",largeurFenetre*0.8,hauteurFenetre*0.8)
        
        #Tableau des scores
        self.tableau = TableauScore(self.fenetre)

    def run(self):
        mainloop = True
        while mainloop:
            for event in pygame.event.get():   
                if event.type == QUIT:               #@UndefinedVariable
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.preselec_btnRetour == True : #@UndefinedVariable
                    bouton.playClickSound()
                    mainloop = False
                    
            self.fenetre.blit(self.background,(0,0))        
            
            #Affichage des éléments
            
            self.tableau.afficher()
            self.panneau.afficher()
            
            
            #Gestion de la selection du bouton
            cursor_pos = pygame.mouse.get_pos()
            self.preselec_button = False
            self.btn_retour.afficher()
            isPreselec = self.btn_retour.isPreselec(cursor_pos)
            if isPreselec :
                self.preselec_btnRetour = True 
            else :
                self.preselec_btnRetour = False 
                
            pygame.display.flip()
            