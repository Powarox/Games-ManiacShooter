import pygame #  @UnusedImport
from pygame.locals import * # @UnusedWildImport
import constantes

from jeu.partie import * # @UnusedWildImport
from interface.menu import *
from interface.parametre import Parametre

#Fonction qui met à jour le fichier paramètre
def majParametre():
    fichier = open(constantes.fichierParam, "r")
    dicParam = {}
    for l in fichier :
        l = l.replace("\n","")
        d = l.split("=")
        if d[0].startswith("ratio") :
            dicParam[d[0]] = float(d[1])
        else :
            dicParam[d[0]] = int(d[1])
    fichier.close()
    constantes.para = dicParam.copy()

#MAIN
majParametre()
pygame.init() 

#Initialisation de la fenetre
fenetre = pygame.display.set_mode((constantes.para["largeur"],constantes.para["hauteur"])) 
pygame.display.set_caption("dew u no de wey ?")
icone = pygame.image.load(constantes.image_icone).convert_alpha()
pygame.display.set_icon(icone)
continuer = True 

#Menu
menu = Menu(fenetre)

#Panneau des scores
viewScore = Score(fenetre)

#Panneau parametre
param = Parametre(fenetre)


while continuer:
    menu.run()
    if menu.start_selected: #Si on choisi "jouer" on lance le jeu
        partie = Partie(fenetre)
        partie.run()
        menu.start_selected = False
        
    if menu.score_selected: #Si on choisi "scores" on lance la page des scores
        menu.score_selected = False
        viewScore.tableau.majDonneesTableau()
        viewScore.run()
    if menu.settings_selected :
        menu.settings_selected = False
        
        
        param.run()
        if param.valideNewParam :
            #Si valider, modifier fichier param.txt
            if param.choixResolution.choix != -1 :
                dim = constantes.tabDimension[param.choixResolution.choix].split("*")
            else :
                dim = (constantes.para["largeur"],constantes.para["hauteur"])
            newDicParam = {"audio":param.case.isValide,
                           "ratioVolMusique":float(param.jaugeVolMusique.percent)/100,
                           "ratioVolJeu":float(param.jaugeVolJeu.percent)/100,
                           "ratioVolInterface":float(param.jaugeVolInterface.percent)/100,
                           "largeur":int(dim[0]),
                           "hauteur":int(dim[1]),
                           "ratioAffichage":int(dim[0])/1200}
            fichier = open(constantes.fichierParam, "w")
            for cle,valeur in newDicParam.items() :
                fichier.write(cle + "=" + str(valeur) + "\n")
            fichier.close()
            majParametre()
            fenetre = pygame.display.set_mode((constantes.para["largeur"],constantes.para["hauteur"])) 
            viewScore = Score(fenetre)
            menu = Menu(fenetre)
        
        param = Parametre(fenetre)
        
        
   
    
        
        
