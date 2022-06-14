import pygame #  @UnusedImport
from pygame.locals import * # @UnusedWildImport
import constantes
from operator import itemgetter

class TableauScore(object):
    def __init__(self,screen):
        self.fenetre = screen
        largeurFenetre = constantes.para["largeur"]
        hauteurFenetre = constantes.para["hauteur"]
        self.police = pygame.font.Font(constantes.gameFont, int(18*constantes.para["ratioAffichage"]))
        self.texteEntete = ((self.police.render("Rang", 1, (255,255,255))),
                            (self.police.render("Joueur", 1, (255,255,255))),
                            (self.police.render("Manches", 1, (255,255,255))),
                            (self.police.render("Points", 1, (255,255,255))))
        
        #Points qui dessinent le tableau
        self.pointsContour = [(largeurFenetre*0.12,hauteurFenetre*0.15),
                              (largeurFenetre*0.88,hauteurFenetre*0.15),
                              (largeurFenetre*0.88,hauteurFenetre*0.70),
                              (largeurFenetre*0.12,hauteurFenetre*0.70)]
        self.pointsEntete = [(self.pointsContour[0][0],self.pointsContour[0][1]*1.3),
                             (self.pointsContour[1][0],self.pointsContour[1][1]*1.3)]
        
        #Coordonnées du texte du tableau
        self.posTextCol1 = (largeurFenetre*0.13,hauteurFenetre*0.16)
        self.posTextCol2 = (largeurFenetre*0.26,hauteurFenetre*0.16)
        self.posTextCol3 = (largeurFenetre*0.54,hauteurFenetre*0.16)
        self.posTextCol4 = (largeurFenetre*0.73,hauteurFenetre*0.16)
        
        #Données du tableau
        self.donnees = []
        
        
    def afficher(self):
        #Dessine les lignes du tableau
        self.bords = pygame.draw.lines(self.fenetre,(255,255,255),True,self.pointsContour,2)
        self.ligneEntete = pygame.draw.lines(self.fenetre,(255,255,255),True,self.pointsEntete,2)
        #Colle les entetes de chaque colonne du tableau
        self.fenetre.blit(self.texteEntete[0],self.posTextCol1)
        self.fenetre.blit(self.texteEntete[1],self.posTextCol2)
        self.fenetre.blit(self.texteEntete[2],self.posTextCol3)
        self.fenetre.blit(self.texteEntete[3],self.posTextCol4) 
        x = 40*constantes.para["ratioAffichage"]        
        rang = 1
        for e in self.donnees :
            classement = (self.police.render(str(rang), 1, (255,255,255)))
            joueur = (self.police.render(e[0], 1, (255,255,255)))
            manche = (self.police.render(e[1], 1, (255,255,255)))
            points = (self.police.render(str(e[2]), 1, (255,255,255)))
            self.fenetre.blit(classement,(self.posTextCol1[0],self.posTextCol1[1]+x))
            self.fenetre.blit(joueur,(self.posTextCol2[0],self.posTextCol2[1]+x))
            self.fenetre.blit(manche,(self.posTextCol3[0],self.posTextCol3[1]+x))
            self.fenetre.blit(points,(self.posTextCol4[0],self.posTextCol4[1]+x))
            x += 40*constantes.para["ratioAffichage"]            
            rang += 1
            
    
    def majDonneesTableau(self) :
        self.donnees.clear()
        self.donnees = recupDonnees()
        
        
def recupDonnees(): #Recupere les données du fichier score
    fichier = open(constantes.fichierScore, "r")
    liste_donnees = []
    for l in fichier :
        l = l.replace("\n","")
        d = l.split(":")
        liste_donnees.append((d[0],d[1],int(d[2])))
    fichier.close()
    liste_donnees.sort(key=itemgetter(2), reverse=True) #Tri dans l'ordre décroissant
    return liste_donnees    
        