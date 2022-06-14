import pygame #  @UnusedImport
from pygame.locals import *
import sys
import constantes
from interface.tableauScore import recupDonnees
from interface import bouton
from jeu.joueur import Joueur
from interface.bouton import Bouton
from jeu.ennemi import placementEnnemi, Ennemi, TirEnnemi
from jeu.effets import Impact, Explosion

class Partie(object):
    
    #Constructeur
    def __init__(self,f):
        
        #Recuperation de certain parametre
        self.largeurFenetre = constantes.para["largeur"]
        self.hauteurFenetre = constantes.para["hauteur"]
        self.ratioAffichage = constantes.para["ratioAffichage"]
        
        #Données membres
        self.fenetre = f                                            #Récupération de la fenêtre
        self.moveBckgr = 0                                          #Initialisation variable qui va gérer le mouvement du background
        self.joueur = Joueur()                                      #Création du joueur
        self.depEnnemi = (2,0)                                      #Vitesse et direction des déplacement ennemi
        self.vagueEnCours = 0                                       #Indique à quel vague le joueur se trouve
        self.delai_vagueSuivant = 0                                 #Délai de la prochaine vague
        self.finPartie = False 
        
        #Groupes
        self.grp_joueur = pygame.sprite.GroupSingle()               
        self.grp_joueur.add(self.joueur)  
        self.grp_ennemi = pygame.sprite.Group()
        self.grp_tir_ennemi = pygame.sprite.Group()                
        self.grp_explosion = pygame.sprite.Group()
        
        #Musique
        if constantes.para["audio"] :
            self.musique = pygame.mixer.Sound(constantes.son_jeu)
            self.musique.set_volume(constantes.para["ratioVolMusique"])
            self.musique.play()
        
        #Images
        coeur = pygame.image.load(constantes.image_vie).convert_alpha()
        self.img_coeur = pygame.transform.scale(coeur,(int(coeur.get_rect().width*self.ratioAffichage),int(coeur.get_rect().height*self.ratioAffichage)))
        self.background = pygame.image.load(constantes.image_fond).convert()   #Chargement image background
        
        #Police
        self.police = pygame.font.Font(constantes.gameFont, int(23*self.ratioAffichage))
        self.policeDefaite = pygame.font.Font(constantes.gameFont, int(42*self.ratioAffichage))
        self.policeVictoire = pygame.font.Font("font/manche.ttf", int(80*self.ratioAffichage))
        
        #Message fin du jeu
        self.afficheDefaite = self.policeDefaite.render("VOTRE VAISSEAU EST DETRUIT", 1, (196, 17, 17))
        self.afficheVictoire = self.policeVictoire.render("VICTOIRE", 1, (255,255,255))
        
        #Score
        self.verifierScore = False
        self.topScore = False
        self.isSaisie = False
        self.saisiPseudo = ""
        self.delai_curseur = 0
        self.afficheCurseur = True
        
        #Zone saisi pseudo
        self.ecart_largeur = self.largeurFenetre/3
        self.texte = self.police.render("Entrez votre pseudo", 1, (255,255,255))
        self.pointsContour = [(self.ecart_largeur,self.hauteurFenetre*0.6),
                              (self.largeurFenetre-self.ecart_largeur,self.hauteurFenetre*0.6),
                              (self.largeurFenetre-self.ecart_largeur,self.hauteurFenetre*0.65),
                              (self.ecart_largeur,self.hauteurFenetre*0.65)]
        
        #Bouton de fin de partie
        self.btnTerminer = Bouton(self.fenetre,"terminer",(self.largeurFenetre/2,self.hauteurFenetre*0.8))
        self.btnPreselec = False
        
    #Fonctions
    def genererVague(self,nbEnnemi,typeEnnemi): #fonction qui genere une vague d'ennemi selon le nombre d'ennemi souhaiter
        lp = placementEnnemi(nbEnnemi,typeEnnemi)
        for i in range(nbEnnemi) :
            ennemi = Ennemi(lp[i],typeEnnemi)
            self.grp_ennemi.add(ennemi)
        self.grp_ennemi.update()     
        
    def gestionEnnemis(self,posPlayer,depH,depV): #Gère les tirs ennemis et renvoie les coordonnées du prochain déplacement du groupe d'ennemi 
        depasseDroite, depasseGauche,depasseBas, depasseHaut = False, False, False, False
        for ennemi in self.grp_ennemi : 
            if ennemi.delai_tir >= 120 and ennemi.rect.top > 0 : #condition qui créer les tirs ennemi
                tirEnnemi = TirEnnemi(ennemi.rect,posPlayer)
                self.grp_tir_ennemi.add(tirEnnemi)
                ennemi.delai_tir = 0
            colision = pygame.sprite.spritecollideany(ennemi, self.joueur.grp_tir) #gestion des colisions ennemi/tir
            if colision != None :
                ennemi.life -= 1
                self.joueur.score += 10
                impact = Impact(colision.rect.center)
                self.grp_explosion.add(impact)
                colision.kill()
            if ennemi.life == 0 :
                self.joueur.score += 100
                explosion = Explosion(ennemi.rect.center)
                ennemi.kill()
                self.grp_explosion.add(explosion)
                
            if ennemi.rect.top <= 1 :
                depasseHaut = True
            if ennemi.rect.right >= self.largeurFenetre :    
                depasseDroite = True
            if ennemi.rect.left <= 20 :
                depasseGauche = True
            if ennemi.rect.bottom >= self.hauteurFenetre*0.66 :
                depasseBas = True
        if depasseHaut :
            depV = 2
        if depasseBas :
            depV = -2
        if depasseGauche :
            depH = 2
        elif depasseDroite :
            depH = -2
        return(depH,depV) #Renvoie la valeur du déplacement horizontale et verticale   
        
    def deplacerGroupeEnnemi(self,h,v): #Déplace le groupe d'ennemi selon les coordonnées entré en paramètre    
        for ennemi in self.grp_ennemi :
            ennemi.rect = ennemi.rect.move(h,v)   
                   
    def gestionVieJoueur(self) : #Gère la vie du joueur lors des collisions
        colision = pygame.sprite.spritecollideany(self.joueur, self.grp_tir_ennemi) #gestion collision et vie du joueur
        if colision != None :
            self.joueur.vie -= 1
            impact = Impact(colision.rect.center)
            self.grp_explosion.add(impact)
            colision.kill()
        if self.joueur.vie == 0 :
            explosion = Explosion(self.joueur.rect.center)
            self.grp_explosion.add(explosion)        
            
    def gestionVague(self,vague): #Gère les passages des vagues
        if self.grp_ennemi.__len__() == 0 and vague < constantes.vagues.__len__() and vague != -1 :
            self.genererVague(constantes.vagues[vague][0],constantes.vagues[vague][1]) 
            vague += 1
        elif self.grp_ennemi.__len__() == 0 and vague == constantes.vagues.__len__() :
            self.finPartie = True
        return vague            
    
    def defilementBackground(self): #Fait défiler le fond
        rel_depFond = self.moveBckgr % self.background.get_rect().height
        self.fenetre.blit(self.background, (0,rel_depFond - self.background.get_rect().height))
        if rel_depFond < self.hauteurFenetre :
            self.fenetre.blit(self.background, (0,rel_depFond))
        self.moveBckgr += 1
                
    def saisiPseudoJoueur(self):
        saisi = self.police.render(self.saisiPseudo, 1, (255,255,255))
        pygame.draw.lines(self.fenetre,(255,255,255),True,self.pointsContour,2)
        self.fenetre.blit(self.texte,((self.largeurFenetre-self.texte.get_width())/2,self.hauteurFenetre*0.55))
        self.fenetre.blit(saisi,(self.ecart_largeur+10,self.hauteurFenetre*0.6+6))
        #dessiner curseur
        if self.delai_curseur >= 30 :
            self.delai_curseur = 0
            if self.afficheCurseur :
                self.afficheCurseur = False
            else :
                self.afficheCurseur = True
        else :
            self.delai_curseur += 1
        if self.afficheCurseur :
            pygame.draw.line(self.fenetre,(255,255,255), (self.ecart_largeur+saisi.get_width()+12,self.hauteurFenetre*0.6+6), (self.ecart_largeur+saisi.get_width()+12,self.hauteurFenetre*0.65-6)) 
            
    def afficher_BtnFin(self):
        self.btnTerminer.afficher()
        cursor_pos = pygame.mouse.get_pos()
        if self.topScore and self.saisiPseudo.__len__() > 0 :
            self.btnPreselec = self.btnTerminer.isPreselec(cursor_pos)
        elif self.topScore == False :
            self.btnPreselec = self.btnTerminer.isPreselec(cursor_pos)
            
    def enregistrerScore(self):
        scoreJoueur = (self.saisiPseudo,self.vagueEnCours,self.joueur.score)
        self.donnees.append(scoreJoueur)
        self.majFichierScore()
        
    def verifScore(self):
        if self.verifierScore == False :
            self.donnees = recupDonnees()
            if self.donnees.__len__() >= 10 :
                scoreEjecter = None
                for ligne in self.donnees :
                    if self.joueur.score > ligne[2] :
                        scoreEjecter = ligne
                if scoreEjecter != None :
                    self.donnees.remove(scoreEjecter)
                    self.topScore =True
            else :
                self.topScore = True
            self.verifierScore = True
            self.isSaisie = True

    def majFichierScore(self):
        fichier = open(constantes.fichierScore, "w")
        for score in self.donnees :
            fichier.write(score[0] + ":" + str(score[1]) + ":" + str(score[2]) + "\n")
        
            
    def run(self): #Gère la partie
        mainloop = True
        while mainloop :
            pygame.time.Clock().tick(80)
            for event in pygame.event.get():   
                if event.type == QUIT:            # @UndefinedVariable
                    sys.exit()
                #Gere la saisi lors de l'enregistrement du score
                if self.isSaisie and event.type == pygame.KEYDOWN :  # @UndefinedVariable
                    if event.dict['unicode'].isalnum() and self.saisiPseudo.__len__() < 12 : #si appuie sur un caractère alphanum et que la chaine < 12
                        self.saisiPseudo += event.dict['unicode']
                    if event.key == 8 : #Si apuie sur touche effacer
                        self.saisiPseudo = self.saisiPseudo[:-1]
                if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.btnPreselec : #Si on clique sur terminer #@UndefinedVariable
                    if self.topScore :
                        self.enregistrerScore()
                    self.musique.stop()
                    bouton.playClickSound()
                    mainloop = False      
            self.defilementBackground()
            
            #Affiche le nombre de vie
            self.afficheVie = self.police.render("{0}".format(self.joueur.vie), 1, (255,255,255))
            self.fenetre.blit(self.afficheVie,(self.largeurFenetre*0.95,5)) 
            self.fenetre.blit(self.img_coeur,(self.largeurFenetre*0.97,5)) #Affiche le coeur à coté
            #Affiche la vague en cours
            textVague = "Vague {0} / {1}".format(self.vagueEnCours,constantes.vagues.__len__())
            self.afficheVague = self.police.render(textVague, 1, (255,255,255))
            #Affiche le score
            self.afficheScore = self.police.render("{0}".format(self.joueur.score), 1, (255,255,255))
            self.fenetre.blit(self.afficheScore,(10,5)) 
            
            if self.joueur.vie > 0 and self.finPartie == False : #Si le joueur a des vies, la partie continue
                self.joueur.controleJoueur()
                self.gestionVieJoueur()
                self.depEnnemi = self.gestionEnnemis(self.joueur.rect, self.depEnnemi[0], self.depEnnemi[1])
                self.deplacerGroupeEnnemi(self.depEnnemi[0], self.depEnnemi[1])    
                self.vagueEnCours = self.gestionVague(self.vagueEnCours)
                self.joueur.grp_tir.update()
                self.joueur.grp_tir.draw(self.fenetre)
                self.grp_ennemi.update()    
                self.grp_ennemi.draw(self.fenetre)
                self.grp_tir_ennemi.update()
                self.grp_tir_ennemi.draw(self.fenetre)
                self.grp_joueur.update()
                self.grp_joueur.draw(self.fenetre)
                
            self.grp_explosion.update()
            self.grp_explosion.draw(self.fenetre)
            
            if self.finPartie or self.joueur.vie <= 0 : #Si condition vrai fin du jeu
                self.verifScore() 
                if self.topScore :
                    self.saisiPseudoJoueur()
                self.afficher_BtnFin()
                if self.finPartie :
                    self.fenetre.blit(self.afficheVictoire,((self.largeurFenetre-self.afficheVictoire.get_width())/2,self.hauteurFenetre/4))
                elif self.joueur.vie <= 0 : #Si le joueur n'a plus de vie
                    self.joueur.kill()
                    self.fenetre.blit(self.afficheDefaite,((self.largeurFenetre-self.afficheDefaite.get_width())/2,self.hauteurFenetre/4))
            else : #Sinon continue le jeu et affiche la vague en cours
                self.fenetre.blit(self.afficheVague,((self.largeurFenetre-self.afficheVague.get_width())*0.5,5))      
            pygame.display.flip()
                
                
