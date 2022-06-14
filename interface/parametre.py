import pygame
from pygame.locals import * # @UnusedWildImport
import constantes
import sys
from interface.panneau import Panneau
from interface.bouton import Bouton
from interface import bouton
from interface.case import Case
from interface.jauge import Jauge
from interface.choixDeroulant import ChoixDeroulant


class Parametre(object):
    def __init__(self,screen):
        self.fenetre = screen
        self.ratioAffichage = constantes.para["ratioAffichage"]
        largeurFenetre = constantes.para["largeur"]
        hauteurFenetre = constantes.para["hauteur"]
        bg = pygame.image.load(constantes.backgroundMenu).convert()
        self.background = pygame.transform.scale(bg,(largeurFenetre,hauteurFenetre))
        self.panneau = Panneau(self.fenetre,"Paramètre",largeurFenetre*0.75,hauteurFenetre*0.75)
        self.btnAnnuler = Bouton(self.fenetre,"Annuler",(largeurFenetre*0.32,hauteurFenetre*0.775))
        self.btnValider = Bouton(self.fenetre,"Valider",(largeurFenetre*0.68,hauteurFenetre*0.775))
        self.preselec = -1
        self.x_lignesParam = largeurFenetre*0.18 #définit les absices des lignes des paramètres
        self.valideNewParam = False
        self.police = pygame.font.Font(constantes.gameFont, int(22*self.ratioAffichage)) 
        
        #Case activer audio
        self.case = Case("Activer le son",self.x_lignesParam,self.panneau.limiteYhaut*1.8,constantes.para["audio"])
        
        #Jauge volume
        x_jauges = largeurFenetre*0.53
        self.y_volMusique = hauteurFenetre*0.3
        self.y_volJeu = hauteurFenetre*0.37
        self.y_volInterface = hauteurFenetre*0.44
        self.jaugeVolMusique = Jauge(constantes.para["ratioVolMusique"]*100,x_jauges,self.y_volMusique)
        self.jaugeVolJeu = Jauge(constantes.para["ratioVolJeu"]*100,x_jauges,self.y_volJeu)
        self.jaugeVolInterface = Jauge(constantes.para["ratioVolInterface"]*100,x_jauges,self.y_volInterface)
        self.texteVolMusique = self.police.render("Volume Musique :", 1, (255,255,255))
        self.texteVolJeu = self.police.render("Volume Jeu :", 1, (255,255,255))
        self.texteVolInterface = self.police.render("Volume Interface :", 1, (255,255,255))
        
        #Resolution
        self.texteResolution = self.police.render("Resolution :", 1, (255,255,255))
        self.y_Resolution = hauteurFenetre*0.52
        self.choixResolution = ChoixDeroulant(constantes.tabDimension,x_jauges,self.y_Resolution,"{0}*{1}".format(largeurFenetre,hauteurFenetre))
        
    def run(self):
        mainloop = True
        while mainloop :
            for event in pygame.event.get():   
                if event.type == QUIT:               #@UndefinedVariable
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.preselec != -1 : #@UndefinedVariable
                    bouton.playClickSound()
                    if self.preselec == 0 : #Si clique bouton annuler
                        mainloop = False
                    if self.preselec == 1 : #Si clique bouton valider
                        self.valideNewParam = True
                        mainloop = False 
                    if self.preselec == 2 : #Si clique case audio
                        self.case.click()
                    if self.preselec == 3 : #Si clique jaugeVolMusique
                        self.jaugeVolMusique.click = True
                    if self.preselec == 4 : #Si clique jaugeVolJeu
                        self.jaugeVolJeu.click = True
                    if self.preselec == 5 : #Si clique jaugeVolInterface
                        self.jaugeVolInterface.click = True
                    if self.preselec == 6 : #Si clique choix Résolution
                        self.choixResolution.clickBtn()  
                    else :
                        self.choixResolution.isActive = False
                    if self.preselec == 7 : #Si clique choix Résolution
                        self.choixResolution.clickChoix()  
                if event.type == MOUSEBUTTONUP and event.button == 1 :  # @UndefinedVariable
                    self.jaugeVolMusique.click = False
                    self.jaugeVolJeu.click = False
                    self.jaugeVolInterface.click = False
            
            #Récupération coordonnées curseur
            cursorPos = pygame.mouse.get_pos()
            
            #Affichage des éléments
            self.fenetre.blit(self.background,(0,0)) 
            self.panneau.afficher()
            self.btnValider.afficher()
            self.btnAnnuler.afficher()
            self.case.afficher(self.fenetre)
            self.jaugeVolMusique.afficher(self.fenetre,cursorPos)
            self.jaugeVolJeu.afficher(self.fenetre,cursorPos)
            self.jaugeVolInterface.afficher(self.fenetre,cursorPos)
            demiHauteur_texte = self.texteVolMusique.get_height()/2
            self.fenetre.blit(self.texteVolMusique,(self.x_lignesParam,self.y_volMusique-demiHauteur_texte))
            self.fenetre.blit(self.texteVolJeu,(self.x_lignesParam,self.y_volJeu-demiHauteur_texte))
            self.fenetre.blit(self.texteVolInterface,(self.x_lignesParam,self.y_volInterface-demiHauteur_texte))
            self.fenetre.blit(self.texteResolution,(self.x_lignesParam,self.y_Resolution-demiHauteur_texte))
            self.choixResolution.afficher(self.fenetre)
            
            #Gestion evenements curseur
            self.preselec = -1
            if self.btnAnnuler.isPreselec(cursorPos) :
                self.preselec = 0
            elif self.btnValider.isPreselec(cursorPos) :
                self.preselec = 1
            elif self.case.isPreselec(cursorPos) :
                self.preselec = 2
            elif self.jaugeVolMusique.isPreselec(cursorPos) :
                self.preselec = 3
            elif self.jaugeVolJeu.isPreselec(cursorPos) :
                self.preselec = 4
            elif self.jaugeVolInterface.isPreselec(cursorPos) :
                self.preselec = 5
            elif self.choixResolution.isBtnPreselec(cursorPos) :
                self.preselec = 6
            elif self.choixResolution.isActive and self.choixResolution.choixPreselec(cursorPos) :
                self.preselec = 7
                
                
            
            pygame.display.flip()

            