import pygame
import sys
import os 
import random
from dossier_chambres import DOSSIER_IMAGE , CHEMIN_IMAGE_FOND , CHEMIN_IMAGE_INTRO , CARTOGRAPHIE_IMAGES_SALLES


class ApplicationPygame:
    # (Le reste de la classe ApplicationPygame n'est pas modifié car la logique de jeu est dans les fonctions globales)
    
    def afficher_introduction(self):
        """Affiche l'écran d'introduction et attend que l'utilisateur appuie sur ENTRÉE."""
        # Tenter de charger l'image d'introduction
        image_intro = None
        try:
            if os.path.exists(CHEMIN_IMAGE_INTRO):
                # Charger et redimensionner l'image pour qu'elle remplisse la fenêtre
                img_pil = pygame.image.load(CHEMIN_IMAGE_INTRO).convert()
                image_intro = pygame.transform.scale(img_pil, (FENETRE_L, FENETRE_H))
            else:
                print(f"ATTENTION: Image d'introduction non trouvée: {CHEMIN_IMAGE_INTRO}. Utilisation d'un fond noir.")
        except pygame.error as e:
            print(f"Erreur de chargement de l'image d'introduction: {e}. Utilisation d'un fond noir.")

        intro = True
        while intro:
            for événement in pygame.event.get():
                if événement.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if événement.type == pygame.KEYDOWN:
                    if événement.key == pygame.K_RETURN:
                        intro = False # Quitter la boucle d'intro si ENTRÉE est pressée

            # Dessin de l'écran d'introduction
            if image_intro:
                self.ecran.blit(image_intro, (0, 0))
            else:
                self.ecran.fill(COULEUR_FOND_CARTE_PRINCIPALE) # Fond noir si l'image manque

            # Texte "Appuyez sur Entrée"
            texte_prompt = "PRESSEZ [ENTRÉE] POUR COMMENCER"
            surface_prompt = self.police_g.render(texte_prompt, True, JAUNE)
            rect_prompt = surface_prompt.get_rect(center=(FENETRE_L // 2, FENETRE_H - 50))
            
            # Dessiner un fond semi-transparent pour le texte (facultatif mais recommandé pour la lisibilité)
            fond_prompt = pygame.Surface((rect_prompt.width + 20, rect_prompt.height + 10), pygame.SRCALPHA)
            fond_prompt.fill((0, 0, 0, 180)) # Noir semi-transparent
            self.ecran.blit(fond_prompt, (rect_prompt.left - 10, rect_prompt.top - 5))

            self.ecran.blit(surface_prompt, rect_prompt)
            
            pygame.display.flip()
            HORLOGE.tick(IPS)

    def __init__(self, ecran):
        self.ecran = ecran
        self.LIGNES, self.COLONNES = 9, 5
        self.joueur = Joueur(pas_départ=70)
        self.donjon = configurer_donjon(self.LIGNES, self.COLONNES)
        self.police_p = pygame.font.Font(None, 18)
        self.police_m = pygame.font.Font(None, 24)
        self.police_g = pygame.font.Font(None, 36)
        self.police_tg = pygame.font.Font(None, 48)
        self.police_symbole = pygame.font.SysFont('Segoe UI Emoji', 24)

        # Définitions des dimensions
        
        # 1. TAILLES FIXES ET AGRANDIES
        self.TAILLE_IMAGE_SALLE_CARTE = 64

        self.TAILLE_IMAGE_PROPOSITION_CARTE = 180

        # 2. DIMENSIONS DE LA CARTE (MAP_RECT -> RECT_CARTE)
        self.MARGE = 20
        self.CELLULE_L = self.TAILLE_IMAGE_SALLE_CARTE + 8
        self.CELLULE_H = self.TAILLE_IMAGE_SALLE_CARTE + 8
        
        carte_l = self.COLONNES * self.CELLULE_L + 2 * self.MARGE
        carte_h = self.LIGNES * self.CELLULE_H + 2 * self.MARGE
        self.RECT_CARTE = pygame.Rect(12, 12, carte_l, carte_h)

        # 3. DIMENSIONS DU PANNEAU (PANEL_RECT -> RECT_PANNEAU)
        self.RECT_PANNEAU = pygame.Rect(self.RECT_CARTE.right + 12, 12, FENETRE_L - self.RECT_CARTE.right - 24, 680)

        # Bouton Redraw (RECT_REDESSINER)
        self.RECT_REDESSINER_BOUTON = pygame.Rect(
            self.RECT_PANNEAU.x + self.RECT_PANNEAU.width - 160 - 24,
            self.RECT_PANNEAU.y + 180 + 6 + 48,
            150, 40)

        # 4. RECTANGLES DE CARTES (RECTS_CARTES)
        self.RECTS_CARTES = []
        ESPACE_CARTES_L = self.RECT_PANNEAU.width - 50
        ECART_CARTES = 5
        self.CADRE_CARTE_L = (ESPACE_CARTES_L - 5 * ECART_CARTES) // 3
        
        # Correction de la hauteur pour un meilleur ajustement du texte
        HAUTEUR_TOTALE_CARTE = self.TAILLE_IMAGE_PROPOSITION_CARTE + 200 
        
        base_x = self.RECT_PANNEAU.x + 24
        for i in range(3):
            x = base_x + i * (self.CADRE_CARTE_L + ECART_CARTES)
            y = self.RECT_PANNEAU.y + 200 + 80
            self.RECTS_CARTES.append(pygame.Rect(x, y, self.CADRE_CARTE_L, HAUTEUR_TOTALE_CARTE))

        self.images = self._charger_images()
        
        self.action = None
        self.cible = None
        self.propositions = []
        self.direction_selectionnee = None
        self.dernier_butin_texte = "—"
        self.boite_message = None

    def _charger_images(self):
        cache_images = {}
        
        # 1. Fond
        try:
            chemin_fond = CHEMIN_IMAGE_FOND
            if os.path.exists(chemin_fond):
                img = pygame.image.load(chemin_fond).convert_alpha()
                cache_images['FOND'] = pygame.transform.scale(img, (self.RECT_CARTE.width, self.RECT_CARTE.height))
            else:
                print(f"ATTENTION: Image de fond non trouvée: {chemin_fond}")
        except pygame.error as e:
            print(f"Erreur de chargement de l'image de fond: {e}")

        # 2. Images de Salle
        for nom, chemin in CARTOGRAPHIE_IMAGES_SALLES.items():
            try:
                if os.path.exists(chemin):
                    img = pygame.image.load(chemin).convert_alpha()
                    w, h = img.get_size()
                    m = min(w, h)
                    img_rognee = img.subsurface(pygame.Rect((w - m) // 2, (h - m) // 2, m, m))
                    
                    # Deux versions de l'image
                    cache_images[f"{nom}_carte"] = pygame.transform.scale(img_rognee, (self.TAILLE_IMAGE_SALLE_CARTE, self.TAILLE_IMAGE_SALLE_CARTE))
                    cache_images[f"{nom}_proposition"] = pygame.transform.scale(img_rognee, (self.TAILLE_IMAGE_PROPOSITION_CARTE, self.TAILLE_IMAGE_PROPOSITION_CARTE))
                else:
                    cache_images[f"{nom}_carte"] = self._créer_surface_substitut(nom, self.TAILLE_IMAGE_SALLE_CARTE)
                    cache_images[f"{nom}_proposition"] = self._créer_surface_substitut(nom, self.TAILLE_IMAGE_PROPOSITION_CARTE)
            except pygame.error:
                cache_images[f"{nom}_carte"] = self._créer_surface_substitut(nom, self.TAILLE_IMAGE_SALLE_CARTE)
                cache_images[f"{nom}_proposition"] = self._créer_surface_substitut(nom, self.TAILLE_IMAGE_PROPOSITION_CARTE)

        return cache_images

    def _créer_surface_substitut(self, nom, taille, est_spéciale=False):
        surface = pygame.Surface((taille, taille))
        surface.fill(BLEU)
        couleur = BLEU_FONCE if est_spéciale else MARRON_FONCE
        pygame.draw.rect(surface, couleur, (5, 5, taille - 10, taille - 10), 0)
        pygame.draw.rect(surface, COULEUR_ACCENT, (5, 5, taille - 10, taille - 10), 3)

        texte = [nom, "(PAS IMAGE)"]
        police_à_utiliser = self.police_p if taille < 100 else self.police_m
        for i, ligne in enumerate(texte):
            surface_texte = police_à_utiliser.render(ligne, True, COULEUR_TEXTE)
            rect_texte = surface_texte.get_rect(center=(taille // 2, taille // 2 + i * (police_à_utiliser.get_height() + 2) - (police_à_utiliser.get_height())))
            surface.blit(surface_texte, rect_texte)
        return surface

    def _dessiner_texte(self, surface, texte, pos, police, couleur=COULEUR_TEXTE, ancre="topleft"):
        surface_texte = police.render(texte, True, couleur)
        rect_texte = surface_texte.get_rect(**{ancre: pos})
        surface.blit(surface_texte, rect_texte)
        return rect_texte

    def _dessiner_carte(self):
        pygame.draw.rect(self.ecran, COULEUR_FOND_CARTE_PRINCIPALE, self.RECT_CARTE)
        if 'FOND' in self.images:
            self.ecran.blit(self.images['FOND'], self.RECT_CARTE.topleft)
        
        for y in range(self.LIGNES):
            for x in range(self.COLONNES):
                x1 = self.RECT_CARTE.x + self.MARGE + x * self.CELLULE_L
                y1 = self.RECT_CARTE.y + self.MARGE + y * self.CELLULE_H
                x2 = x1 + self.CELLULE_L
                y2 = y1 + self.CELLULE_H
                
                rect_cellule = pygame.Rect(x1, y1, self.CELLULE_L, self.CELLULE_H)
                salle = self.donjon[y][x]

                couleur_contour = (51, 51, 51); épaisseur_contour = 1
                if y == self.joueur.pos_y and x == self.joueur.pos_x:
                    couleur_contour = COULEUR_ACCENT; épaisseur_contour = 3
                pygame.draw.rect(self.ecran, couleur_contour, rect_cellule, épaisseur_contour)

                if salle is not None:
                    nom_salle = salle.nom.upper()
                    img_salle = self.images.get(f"{nom_salle}_carte")
                    if img_salle is None:
                        img_salle = self._créer_surface_substitut(nom_salle, self.TAILLE_IMAGE_SALLE_CARTE, salle.type_salle == "special")
                        self.images[f"{nom_salle}_carte"] = img_salle
                        
                    rect_image = img_salle.get_rect(center=rect_cellule.center)
                    self.ecran.blit(img_salle, rect_image.topleft)

                    épaisseur_porte = 4
                    couleur_porte = JAUNE if salle.type_salle == "special" else COULEUR_TEXTE
                    if salle.sorties.get("haut"): pygame.draw.line(self.ecran, couleur_porte, (x1 + self.CELLULE_L / 3, y1), (x2 - self.CELLULE_L / 3, y1), épaisseur_porte)
                    if salle.sorties.get("bas"): pygame.draw.line(self.ecran, couleur_porte, (x1 + self.CELLULE_L / 3, y2), (x2 - self.CELLULE_L / 3, y2), épaisseur_porte)
                    if salle.sorties.get("gauche"): pygame.draw.line(self.ecran, couleur_porte, (x1, y1 + self.CELLULE_H / 3), (x1, y2 - self.CELLULE_H / 3), épaisseur_porte)
                    if salle.sorties.get("droite"): pygame.draw.line(self.ecran, couleur_porte, (x2, y1 + self.CELLULE_H / 3), (x2, y2 - self.CELLULE_H / 3), épaisseur_porte)
                
                if y == self.joueur.pos_y and x == self.joueur.pos_x:
                    self._dessiner_texte(self.ecran, "👤", rect_cellule.center, self.police_tg, JAUNE, ancre="center")

                if self.action == "draft" and self.cible == (y, x):
                    pygame.draw.rect(self.ecran, ROUGE, rect_cellule, 4)
                    self._dessiner_texte(self.ecran, "?", rect_cellule.center, self.police_g, ROUGE, ancre="center")
    
    def _dessiner_panneau(self):
        pygame.draw.rect(self.ecran, COULEUR_FOND_PANNEAU, self.RECT_PANNEAU)
        
        # Inventaire et Ressources 
        inv_rect = pygame.Rect(self.RECT_PANNEAU.x + 24, self.RECT_PANNEAU.y + 16, (self.RECT_PANNEAU.width - 48) // 2, 180)
        self._dessiner_texte(self.ecran, "INVENTAIRE", inv_rect.topleft, self.police_g, COULEUR_TEXTE)
        
        tool_y = inv_rect.top + 40
        for outil in self.joueur.ceinture_outils:
            self._dessiner_texte(self.ecran, f" > {outil}", (inv_rect.left, tool_y), self.police_m, (160, 160, 160))
            tool_y += 20
        
        res_rect = pygame.Rect(self.RECT_PANNEAU.x + self.RECT_PANNEAU.width // 2 + 10, self.RECT_PANNEAU.y + 16, self.RECT_PANNEAU.width // 2 - 34, 180)
        self._dessiner_texte(self.ecran, "RESSOURCES", res_rect.topright, self.police_m, (160, 160, 160), ancre="topright")
        
        données_ressources = [
            ("PAS RESTANTS", self.joueur.pas_restants , "🦶", COULEUR_ACCENT),
            ("PIÈCES", self.joueur.inventaire["coins"], "💰", COULEUR_ACCENT ),
            ("GEMMES", self.joueur.inventaire["gems"], "💎", COULEUR_ACCENT),
            ("CLÉS", self.joueur.inventaire["keys"], "🔑", COULEUR_ACCENT),
            ("DÉS", self.joueur.inventaire["dice"], "🎲", COULEUR_ACCENT),
        ]
        
        res_y = res_rect.top + 40
        for texte, valeur, icône, couleur_icône in données_ressources:
            val_surf = self.police_g.render(str(valeur), True, JAUNE)
            val_rect = val_surf.get_rect(right=res_rect.right - 40, top=res_y)
            self.ecran.blit(val_surf, val_rect)
            self._dessiner_texte(self.ecran, texte, (val_rect.left - 4, res_y + 4), self.police_m, COULEUR_TEXTE, ancre="topright")
            self._dessiner_texte(self.ecran, icône, (res_rect.right, res_y + 4), self.police_g, couleur_icône, ancre="topright")
            res_y += 30

        loot_rect = pygame.Rect(self.RECT_PANNEAU.x + 24, self.RECT_PANNEAU.y + 16 + 182, self.RECT_PANNEAU.width - 48, 24)
        self._dessiner_texte(self.ecran, f"Dernier butin : {self.dernier_butin_texte}", loot_rect.topleft, self.police_m, (255, 211, 105))
        
        # Zone de Draft 
        draft_y = self.RECT_PANNEAU.y + 240
        
        titre_texte = "Explorer ou attendre"
        titre_couleur = COULEUR_TEXTE
        if self.action == "draft":
            titre_texte = "CHOISISSEZ UNE SALLE "
            titre_couleur = JAUNE
        
        self._dessiner_texte(self.ecran, titre_texte, (self.RECT_PANNEAU.x + 24, draft_y + 10), self.police_g, titre_couleur)

        if self.action == "draft":
            pygame.draw.rect(self.ecran, COULEUR_ACCENT if self.joueur.inventaire["dice"] > 0 else (60, 60, 60), self.RECT_REDESSINER_BOUTON, 0, 5)
            self._dessiner_texte(self.ecran, "🎲 Redraw (D)", self.RECT_REDESSINER_BOUTON.center, self.police_m, COULEUR_FOND_CARTE_PRINCIPALE, ancre="center")
            
            for i, r in enumerate(self.propositions):
                rect_carte = self.RECTS_CARTES[i]
                
                pygame.draw.rect(self.ecran, COULEUR_FOND_CARTE, rect_carte, 0, 5)
                
                nom_salle = r.nom.upper()
                img_salle = self.images.get(f"{nom_salle}_proposition")
                if img_salle is None:
                    img_salle = self._créer_surface_substitut(nom_salle, self.TAILLE_IMAGE_PROPOSITION_CARTE, r.type_salle == "special")
                    self.images[f"{nom_salle}_proposition"] = img_salle
                
                rect_image = img_salle.get_rect(centerx=rect_carte.centerx, top=rect_carte.top + 8 + self.TAILLE_IMAGE_PROPOSITION_CARTE // 2)
                self.ecran.blit(img_salle, rect_image.topleft)

                lines = [r.nom, f"TYPE: {r.type_salle.upper()}"]
                if r.type_salle == "special": lines.append(f"COÛT: {r.cout}C")
                if r.frais_entrée > 0: lines.append(f"FRAIS: {r.frais_entrée}C POUR ENTRER")
                
                # ajustement des lignes : Utilisation de la hauteur de la police
                rareté = CARTOGRAPHIE_RARETE.get(r.nom.upper(), 0)
                lines.append(f"RARETÉ: {rareté}") # Affiche le degré de rareté
                
                hauteur_ligne = self.police_m.get_height() + 2 # Hauteur de la police + 2px de marge
                desc_y = rect_image.bottom + 10
                for j, ligne in enumerate(lines):
                    y_pos = desc_y + j * hauteur_ligne
                    self._dessiner_texte(self.ecran, ligne, (rect_carte.left + 8, y_pos), self.police_m, COULEUR_TEXTE)

                hint_rect = pygame.Rect(rect_carte.left, rect_carte.bottom - 25, rect_carte.width, 20)
                self._dessiner_texte(self.ecran, f"PRESSEZ [{i+1}]", hint_rect.center, self.police_p, COULEUR_ACCENT, ancre="center")

        if self.boite_message:
            self._dessiner_boîte_message()

    def _dessiner_boîte_message(self):
        overlay = pygame.Surface((FENETRE_L, FENETRE_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.ecran.blit(overlay, (0, 0))

        titre, texte = self.boite_message
        boite_l, boite_h = 800, 200
        rect_boite = pygame.Rect((FENETRE_L - boite_l) // 2, (FENETRE_H - boite_h) // 2, boite_l, boite_h)
        pygame.draw.rect(self.ecran, COULEUR_FOND_PANNEAU, rect_boite, 0, 10)
        pygame.draw.rect(self.ecran, COULEUR_ACCENT, rect_boite, 3, 10)

        self._dessiner_texte(self.ecran, titre, (rect_boite.centerx, rect_boite.top + 20), self.police_g, JAUNE, ancre="center")
        self._dessiner_texte(self.ecran, texte, (rect_boite.centerx, rect_boite.top + 70), self.police_m, COULEUR_TEXTE, ancre="center")

        rect_ok = pygame.Rect(rect_boite.centerx - 50, rect_boite.bottom - 50, 100, 30)
        pygame.draw.rect(self.ecran, COULEUR_ACCENT, rect_ok, 0, 5)
        self._dessiner_texte(self.ecran, "OK", rect_ok.center, self.police_m, COULEUR_FOND_CARTE_PRINCIPALE, ancre="center")
        self.rect_ok_boite_message = rect_ok

    def _définir_dernier_butin(self, gagne: dict):
        parties = []
        for k in ("pieces", "coins", "gems", "keys", "dice"):
            if gagne.get(k, 0):
                parties.append(f"{k}+{gagne[k]}")
        if "tools" in gagne and gagne["tools"] is not None and len(gagne["tools"]) > 0:
            parties.append("outils: " + ", ".join(gagne["tools"]))
        self.dernier_butin_texte = ", ".join(parties) if parties else "—"

    def _vérifier_victoire(self):
        """Vérifie si le joueur est entré dans la salle ANTECHAMBER (position 0, 2)."""
        if self.joueur.pos_y == 0 and self.joueur.pos_x == 2:
            self.boite_message = ("VICTOIRE !", "Bravo champion, vous avez atteint l'ANTECHAMBER !")
            self.joueur.pas_restants = 0
            self.action = None
            return True
        return False

    def _gérer_sélection_salle_draft(self, index):
        global PIECES_DISPONIBLES
        
        if index >= len(self.propositions):
            return
        
        y, x = self.cible
        salle_choisie = self.propositions[index]

        if not self.joueur.se_déplacer():
            self.boite_message = ("Déplacement Impossible", "Plus de pas restants !")
            self.action = None; return

        if salle_choisie.type_salle == "special" and not self.joueur.payer("coins", 3):
            self.boite_message = ("Pièce Spéciale", "Pas assez de Pièces (3 Pièce). Annulation du placement.")
            self.joueur.pas_restants += 1
            self.action = None; return

        if salle_choisie.frais_entrée > 0:
            if not self.joueur.payer("coins", salle_choisie.frais_entrée):
                self.boite_message = ("Salle Payante", f"Besoin de {salle_choisie.frais_entrée} pièces pour entrer. Placement annulé.")
                self.joueur.pas_restants += 1
                self.action = None; return

        # Règle 2: Retrait de la Pioche 
        # Si la salle est placée, elle est retirée des options de tirage futures.
        if salle_choisie.nom.upper() in PIECES_DISPONIBLES:
            PIECES_DISPONIBLES.remove(salle_choisie.nom.upper())
        # -------------------------------------

        self.donjon[y][x] = salle_choisie
        self.joueur.pos_y, self.joueur.pos_x = y, x

        gagne = self.joueur.collecter(salle_choisie)
        if gagne:
            self._définir_dernier_butin(gagne)
            self.boite_message = ("Collecté", f"Vous avez trouvé : {gagne}")
            
        # Vérifie la victoire après avoir placé la salle
        if self._vérifier_victoire():
            return

        self.action = None
        self.cible = None
        self.propositions = []
        self.direction_selectionnee = None

        

    def _gérer_mouvement(self, cle):
        py, px = self.joueur.pos_y, self.joueur.pos_x
        
        if self.action == "draft":
            self.action = None
            self.cible = None
            self.propositions = []
            self.direction_selectionnee = None
            return

        dy, dx = {"haut": (-1,0), "bas": (1,0), "gauche": (0,-1), "droite": (0,1)}[cle]
        ny, nx = py+dy, px+dx
        
        if not (0 <= ny < self.LIGNES and 0 <= nx < self.COLONNES):
            return
        
        salle_actuelle = self.donjon[py][px]
        
        if self.donjon[ny][nx] is None:
            if salle_actuelle and salle_actuelle.sorties.get(cle, False):
                self.action = "draft"
                self.direction_selectionnee = cle
                self.propositions = générer_propositions_uniques(ny, nx, cle, compte=3)
                self.cible = (ny, nx)
            else:
                self.boite_message = ("Bloqué", "Impossible de construire une pièce ici (pas de sortie dans la pièce actuelle).")
        else:
            salle_cible = self.donjon[ny][nx]
            salle_actuelle_ouverte = salle_actuelle.sorties.get(cle, False)
            salle_cible_ouverte = salle_cible.sorties.get(_obtenir_direction_opposée(cle), False)
            
            if salle_actuelle_ouverte and salle_cible_ouverte:
                if self.joueur.se_déplacer():
                    self.joueur.pos_y, self.joueur.pos_x = ny, nx
                    gagne = self.joueur.collecter(self.donjon[ny][nx])
                    if gagne:
                        self._définir_dernier_butin(gagne)
                        self.boite_message = ("Collecté", f"Vous avez trouvé : {gagne}")

                    # Vérifie la victoire après le déplacement
                    if self._vérifier_victoire():
                        return
                else:
                    self.boite_message = ("Déplacement Impossible", "Plus de pas restants!")
            else:
                self.boite_message = ("Bloqué", "Ce mur est un cul-de-sac (portes non alignées).")
        
        if self.action != "draft":
            self.propositions = []
            self.cible = None
            self.direction_selectionnee = None

    def _gérer_redessiner(self):
        if self.action == "draft" and self.joueur.inventaire["dice"] > 0 and self.cible:
            if not self.direction_selectionnee:
                self.boite_message = ("Erreur", "Direction de draft manquante pour le Redraw.")
                return
            self.joueur.inventaire["dice"] -= 1
            y, x = self.cible
            self.propositions = générer_propositions_uniques(y, x, self.direction_selectionnee, compte=3)
        else:
            self.boite_message = ("Redraw", "Pas de dé restant ou pas en mode Draft.")

    def gérer_événement(self, événement):
        if self.boite_message:
            if événement.type == pygame.MOUSEBUTTONDOWN and self.rect_ok_boite_message.collidepoint(événement.pos):
                self.boite_message = None
            if événement.type == pygame.KEYDOWN and événement.key == pygame.K_RETURN:
                 self.boite_message = None
            return

        if événement.type == pygame.KEYDOWN:
            if événement.key == pygame.K_UP: self._gérer_mouvement("haut")
            elif événement.key == pygame.K_DOWN: self._gérer_mouvement("bas")
            elif événement.key == pygame.K_LEFT: self._gérer_mouvement("gauche")
            elif événement.key == pygame.K_RIGHT: self._gérer_mouvement("droite")
            elif self.action == "draft":
                if événement.key == pygame.K_1: self._gérer_sélection_salle_draft(0)
                elif événement.key == pygame.K_2: self._gérer_sélection_salle_draft(1)
                elif événement.key == pygame.K_3: self._gérer_sélection_salle_draft(2)
                elif événement.key == pygame.K_d: self._gérer_redessiner()
        
        elif événement.type == pygame.MOUSEBUTTONDOWN and événement.button == 1:
            if self.RECT_REDESSINER_BOUTON.collidepoint(événement.pos) and self.action == "draft" and self.joueur.inventaire["dice"] > 0:
                self._gérer_redessiner()
            
            elif self.action == "draft":
                for i, rect in enumerate(self.RECTS_CARTES):
                    if rect.collidepoint(événement.pos):
                        self._gérer_sélection_salle_draft(i)
                        break

    def exécuter(self):
        running = True
        while running:
            for événement in pygame.event.get():
                if événement.type == pygame.QUIT:
                    running = False
                self.gérer_événement(événement)

            # Vérifie le Game Over/Victoire (si la boîte de message n'est pas déjà affichée)
            if self.joueur.pas_restants <= 0 and self.boite_message is None:
                # Vérifie si la fin n'est pas déjà l'ANTECHAMBER
                if self.joueur.pos_y != 0 or self.joueur.pos_x != 2:
                    self.boite_message = ("GAME OVER", "Plus de pas restants. Le jeu est terminé.")
            
            self.ecran.fill(COULEUR_FOND_CARTE_PRINCIPALE)
            self._dessiner_carte()
            self._dessiner_panneau()
            
            pygame.display.flip()
            HORLOGE.tick(IPS)

        pygame.quit()
        sys.exit()