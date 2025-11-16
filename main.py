import os
import random
import pygame
import sys
from chambres_portes import DEFAULT_EXITS

# Configuration de Pygame
pygame.init()

#  Constantes Pygame 
FENETRE_L, FENETRE_H = 1200, 720
ECRAN = pygame.display.set_mode((FENETRE_L, FENETRE_H))
pygame.display.set_caption(" Draft des Salles (Pygame)")
HORLOGE = pygame.time.Clock()
IPS = 60

#  Couleurs 
COULEUR_TEXTE = (224, 224, 224)
COULEUR_ACCENT = (0, 255, 0)
COULEUR_FOND_PANNEAU = (30, 30, 30)
COULEUR_FOND_CARTE = (42, 42, 42)
COULEUR_FOND_CARTE_PRINCIPALE = (0, 0, 0)
JAUNE = (255, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (30, 30, 40)
BLEU_FONCE = (40, 60, 100)
MARRON_FONCE = (70, 45, 30)

#  Dossiers/Images 

DOSSIER_IMAGE = "images projet"
CHEMIN_IMAGE_FOND = os.path.join(DOSSIER_IMAGE, "image arriere .plan.png")

# Les images de salle
CHEMIN_IMAGE_INTRO = os.path.join(DOSSIER_IMAGE, "image introduction du jeu.png")
CARTOGRAPHIE_IMAGES_SALLES = {
   "THE FOUNDATION": os.path.join(DOSSIER_IMAGE, "THE FOUNDATION.png"),
    "ENTRANCE HALL": os.path.join(DOSSIER_IMAGE, "ENTRANCE HALL.png"), 
    "SPARE ROOM": os.path.join(DOSSIER_IMAGE, "SPARE ROOM.png"),
    "ROTUNDA": os.path.join(DOSSIER_IMAGE, "ROTUNDA.png"),
    "PARLOR": os.path.join(DOSSIER_IMAGE, "PARLOR.png"),
    "BILLIARD ROOM": os.path.join(DOSSIER_IMAGE, "BILLIARD ROOM.png"),
    "GALLERY": os.path.join(DOSSIER_IMAGE, "GALLERY.png"),
    "ROOM8": os.path.join(DOSSIER_IMAGE, "ROOM8.png"),
    "CLOSET": os.path.join(DOSSIER_IMAGE, "CLOSET.png"),
    "WALK IN CLOSET": os.path.join(DOSSIER_IMAGE, "WALK IN CLOSET.png"),
    "ATTIC": os.path.join(DOSSIER_IMAGE, "ATTIC.png"),
    "STOREROOM": os.path.join(DOSSIER_IMAGE, "STOREROOM.png"),
    "NOOK": os.path.join(DOSSIER_IMAGE, "NOOK.png"),
    "GARAGE": os.path.join(DOSSIER_IMAGE, "GARAGE.png"),
    "MUSIC ROOM": os.path.join(DOSSIER_IMAGE, "MUSIC ROOM.png"),
    "LOCKER ROOM": os.path.join(DOSSIER_IMAGE, "LOCKER ROOM.png"),
    "DEN": os.path.join(DOSSIER_IMAGE, "DEN.png"),
    "WINE CELLAR": os.path.join(DOSSIER_IMAGE, "WINE CELLAR.png"),
    "TROPHY ROOM": os.path.join(DOSSIER_IMAGE, "TROPHY ROOM.png"),
    "BALLROOM": os.path.join(DOSSIER_IMAGE, "BALLROOM.png"),
    "PANTRY": os.path.join(DOSSIER_IMAGE, "PANTRY.png"),
    "RUMPUS ROOM": os.path.join(DOSSIER_IMAGE, "RUMPUS ROOM.png"),
    "VAULT": os.path.join(DOSSIER_IMAGE, "VAULT.png"),
    "OFFICE": os.path.join(DOSSIER_IMAGE, "OFFICE.png"),
    "DRAWING ROOM": os.path.join(DOSSIER_IMAGE, "DRAWING ROOM.png"),
    "STUDY": os.path.join(DOSSIER_IMAGE, "STUDY.png"),
    "LIBRARY": os.path.join(DOSSIER_IMAGE, "LIBRARY.png"),
    "CHAMBER OF MIRRORS": os.path.join(DOSSIER_IMAGE, "CHAMBER OF MIRRORS.png"),
    "THE POOL": os.path.join(DOSSIER_IMAGE, "THE POOL.png"), 
    "DRAFTING STUDIO": os.path.join(DOSSIER_IMAGE, "DRAFTING STUDIO.png"),
    "UTILITY CLOSET": os.path.join(DOSSIER_IMAGE, "UTILITY CLOSET.png"),
    "BOILER ROOM": os.path.join(DOSSIER_IMAGE, "BOILER ROOM.png"), 
    "PUMP ROOM": os.path.join(DOSSIER_IMAGE, "PUMP ROOM.png"),
    "SECURITY": os.path.join(DOSSIER_IMAGE, "SECURITY.png"),
    "WORKSHOP": os.path.join(DOSSIER_IMAGE, "WORKSHOP.png"), 
    "LABORATORY": os.path.join(DOSSIER_IMAGE, "LABORATORY.png"),
    "SAUNA": os.path.join(DOSSIER_IMAGE, "SAUNA.png"), 
    "COAT CHECK": os.path.join(DOSSIER_IMAGE, "COAT CHECK.png"), 
    "MAIL ROOM": os.path.join(DOSSIER_IMAGE, "MAIL ROOM.png"), 
    "FREEZER": os.path.join(DOSSIER_IMAGE, "FREEZER.png"), 
    "DINNING ROOM": os.path.join(DOSSIER_IMAGE, "DINNING ROOM.png"),
    "OBSERVATORY": os.path.join(DOSSIER_IMAGE, "OBSERVATORY.png"),
    "CONFERENCE ROOM": os.path.join(DOSSIER_IMAGE, "CONFERENCE ROOM.png"),
    "AQUARIUM": os.path.join(DOSSIER_IMAGE, "AQUARIUM.png"),
    "ANTECHAMBER": os.path.join(DOSSIER_IMAGE, "ANTECHAMBER.png"),

    # pièces violettes
    "BEDROOM": os.path.join(DOSSIER_IMAGE, "BEDROOM.png"),
    "BOUDOIR": os.path.join(DOSSIER_IMAGE, "BOUDOIR.png"),
    "GUEST BEDROOM": os.path.join(DOSSIER_IMAGE, "GUEST BEDROOM.png"),
    "NURSERY": os.path.join(DOSSIER_IMAGE, "NURSERY.png"),
    "SERVANT'S QUARTERS": os.path.join(DOSSIER_IMAGE, "SERVANT'S QUARTERS.png"),
    "BUNK ROOM": os.path.join(DOSSIER_IMAGE, "BUNK ROOM.png"),
    "THE LADY CHIP'S CHAMBER": os.path.join(DOSSIER_IMAGE, "THE LADY CHIP'S CHAMBER.png"),
    "MASTER BEDROOM": os.path.join(DOSSIER_IMAGE, "MASTER BEDROOM.png"),

    # pièces marrons
    "HALLWAY": os.path.join(DOSSIER_IMAGE, "HALLWAY.png"), 
    "WEST WING HALL": os.path.join(DOSSIER_IMAGE, "WEST WING HALL.png"),
    "EAST WING HALL": os.path.join(DOSSIER_IMAGE, "EAST WING HALL.png"),
    "CORRIDOR": os.path.join(DOSSIER_IMAGE, "CORRIDOR.png"), 
    "PASSAGE WAY": os.path.join(DOSSIER_IMAGE, "PASSAGEWAY.png"), 
    "SECRET PASSAGE": os.path.join(DOSSIER_IMAGE, "SECRET PASSAGE.png"),
    "FOYER": os.path.join(DOSSIER_IMAGE, "FOYER.png"),
    "GREAT HALL": os.path.join(DOSSIER_IMAGE, "GREAT HALL.png"),

    # pièces vertes
    "TERRACE": os.path.join(DOSSIER_IMAGE, "TERRACE.png"),
    "PATIO": os.path.join(DOSSIER_IMAGE, "PATIO.png"),
    "COURTYARD": os.path.join(DOSSIER_IMAGE, "COURTYARD.png"),
    "CLOISTER": os.path.join(DOSSIER_IMAGE, "CLOISTER.png"),
    "VERANDA": os.path.join(DOSSIER_IMAGE, "VERANDA.png"),
    "GREENHOUSE": os.path.join(DOSSIER_IMAGE, "GREENHOUSE.png"),
    "MORNING ROOM": os.path.join(DOSSIER_IMAGE, "MORNING ROOM.png"),
    "SECRET GARDEN": os.path.join(DOSSIER_IMAGE, "SECRET GARDEN.png"),

    # pièces jaunes
    "COMMISSARY": os.path.join(DOSSIER_IMAGE, "COMMISSARY.png"),
    "KITCHEN": os.path.join(DOSSIER_IMAGE, "KITCHEN.png"),
    "LOCKSMITH": os.path.join(DOSSIER_IMAGE, "LOCKSMITH.png"),
    "SHOWROOM": os.path.join(DOSSIER_IMAGE, "SHOWROOM.png"),
    "LAUNDRY ROOM": os.path.join(DOSSIER_IMAGE, "LAUNDRY ROOM.png"),
    "BOOKSHOP": os.path.join(DOSSIER_IMAGE, "BOOKSHOP.png"),
    "THE ARMORY": os.path.join(DOSSIER_IMAGE, "THE ARMORY.png"),
    "MOUNT HOLLY GIFT SHOP": os.path.join(DOSSIER_IMAGE, "MOUNT HOLLY GIFT SHOP.png"),

    # pièces rouges
    "LAVATORY": os.path.join(DOSSIER_IMAGE, "LAVATORY.png"),
    "CHAPEL": os.path.join(DOSSIER_IMAGE, "CHAPEL.png"),
    "MAID'S CHAMBER": os.path.join(DOSSIER_IMAGE, "MAID'S CHAMBER.png"),
    "ARCHIVES": os.path.join(DOSSIER_IMAGE, "ARCHIVES.png"),
    "GYMNASIUM": os.path.join(DOSSIER_IMAGE, "GYMNASIUM.png"),
    "DARKROOM": os.path.join(DOSSIER_IMAGE, "DARKROOM.png"),
    "WEIGHT ROOM": os.path.join(DOSSIER_IMAGE, "WEIGHTROOM.png"),
    "FURNACE": os.path.join(DOSSIER_IMAGE, "FURNACE.png")
}

TOUS_NOMS_SALLES = [name for name in DEFAULT_EXITS.keys() if name not in {"ENTRANCE HALL", "ANTECHAMBER"}]
POOL_OUTILS = ["Crowbar", "Lockpick", "Torch", "Rope", "Goggles"]

# 1) Modèles de Jeu


class Chambre:
    def __init__(self, x, y, type_salle="standard", ressources=None, sorties=None, nom="SALLE", frais_entrée=0):
        self.pos_x = x
        self.pos_y = y
        self.type_salle = type_salle
        self.cout = 1 if type_salle == "special" else 0
        self.ressources = ressources if ressources is not None else {
            "bread": 0, "coins": 0, "gems": 0, "keys": 0, "dice": 0, "tools": []
        }
        self.sorties = sorties if sorties is not None else {}
        self.visitee = False
        self.nom = nom
        self.frais_entrée = max(0, int(frais_entrée))

class Joueur:
    def __init__(self, pas_départ: int):
        self.pas_restants = pas_départ
        self.inventaire = {"bread": 0, "coins": 5, "gems": 1, "keys": 2, "dice": 3}
        self.ceinture_outils = ["Shovel", "Metal Detector"]
        self.pos_y = 8
        self.pos_x = 1

    def se_déplacer(self):
        if self.pas_restants > 0:
            self.pas_restants -= 1
            return True
        return False

    def payer(self, article, montant):
        if self.inventaire.get(article, 0) >= montant:
            self.inventaire[article] -= montant
            return True
        return False

    def collecter(self, salle):
        if salle.visitee:
            return {}
        gagne = {}
        for k in ("bread", "coins", "gems", "keys", "dice"):
            v = salle.ressources.get(k, 0)
            if v > 0:
                self.inventaire[k] = self.inventaire.get(k, 0) + v
                gagne[k] = v
                salle.ressources[k] = 0
        outils = salle.ressources.get("tools", [])
        if outils:
            gagne["tools"] = []
            for t in outils:
                if t not in self.ceinture_outils:
                    self.ceinture_outils.append(t)
                gagne["tools"].append(t)
            salle.ressources["tools"] = []
        salle.visitee = True
        return gagne



# 2) Génération de Donjon


def _obtenir_direction_opposée(direction):
    opposites = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}
    return opposites.get(direction)

def obtenir_sorties_depuis_modele(nom_salle: str) -> dict:
    modele = DEFAULT_EXITS.get(nom_salle.upper(), {"haut": 1, "bas": 1, "gauche": 1, "droite": 1})
    return {d: bool(v) for d, v in modele.items()}

def générer_salle_aléatoire(y, x):
    est_spéciale = random.random() < 0.3
    type_salle = "special" if est_spéciale else "standard"
    nom = random.choice(TOUS_NOMS_SALLES)
    sorties = obtenir_sorties_depuis_modele(nom)

    base = {"bread": random.randint(0, 1),
            "dice": random.randint(0, 1),
            "coins": random.randint(0, 2),
            "gems": 0,
            "keys": 0,
            "tools": []}

    if est_spéciale:
        base["gems"] = random.randint(1, 2)
        base["keys"] = random.randint(0, 1)

    if nom == "BEDROOM":
        base["dice"] += 2
    elif nom == "DEN":
        base["gems"] += 1
    elif nom == "GUEST BEDROOM":
        base["bread"] += 10
    elif nom == "NOOK":
        base["keys"] += 1
    elif nom == "STOREROOM":
        base["keys"] += 1; base["gems"] += 1; base["coins"] += 1

    chance_outil = 0.15 if est_spéciale else 0.10
    if random.random() < chance_outil:
        n_outils = 2 if (est_spéciale and random.random() < 0.25) else 1
        base["tools"] = random.sample(POOL_OUTILS, k=min(n_outils, len(POOL_OUTILS)))

    frais_entrée = 0
    if random.random() < (0.22 if est_spéciale else 0.15):
        frais_entrée = 1 if not est_spéciale else random.choice([1, 2, 3])

    return Chambre(x, y, type_salle=type_salle, ressources=base, sorties=sorties, nom=nom, frais_entrée=frais_entrée)

def générer_salle_compatible(y, x, direction_depuis_joueur: str):
    sortie_requise = _obtenir_direction_opposée(direction_depuis_joueur)
    salle_compatible = None
    while salle_compatible is None:
        salle_temp = générer_salle_aléatoire(y, x)
        if salle_temp.sorties.get(sortie_requise, False):
            salle_compatible = salle_temp
    return salle_compatible

def générer_propositions_uniques(y, x, direction_depuis_joueur: str, compte=3):
    vu = set(); props = []; essais = 0; max_essais = 80
    while len(props) < compte and essais < max_essais:
        r = générer_salle_compatible(y, x, direction_depuis_joueur)
        if r.nom.upper() not in vu:
            vu.add(r.nom.upper()); props.append(r)
        essais += 1
    return props

def configurer_donjon(lignes=9, colonnes=6):
    grille = [[None for _ in range(colonnes)] for _ in range(lignes)]
    sorties_départ = obtenir_sorties_depuis_modele("ENTRANCE HALL")
    départ = Chambre(1, 8, "standard",
                  ressources={"bread": 1, "coins": 1, "gems": 0, "keys": 0, "dice": 1, "tools": []},
                  sorties=sorties_départ, nom="ENTRANCE HALL", frais_entrée=0)
    départ.visitee = True
    grille[8][1] = départ
    sorties_fin = obtenir_sorties_depuis_modele("ANTECHAMBER")
    fin = Chambre(2, 0, "special",
                ressources={"bread": 3, "coins": 5, "gems": 5, "keys": 2, "dice": 3, "tools": []},
                sorties=sorties_fin, nom="ANTECHAMBER", frais_entrée=0)
    grille[0][2] = fin
    return grille

# 3) Interface Utilisateur Pygame


class ApplicationPygame:

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

            #  Dessin de l'écran d'introduction 
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

        # --- Définitions des dimensions ---
        
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
        
        HAUTEUR_EXTRA_CADRE = 20
        hauteur_totale_carte = self.TAILLE_IMAGE_PROPOSITION_CARTE + 3 * HAUTEUR_EXTRA_CADRE + 2 * 60
        
        base_x = self.RECT_PANNEAU.x + 24
        for i in range(3):
            x = base_x + i * (self.CADRE_CARTE_L + ECART_CARTES)
            y = self.RECT_PANNEAU.y + 200 + 80
            self.RECTS_CARTES.append(pygame.Rect(x, y, self.CADRE_CARTE_L, hauteur_totale_carte))

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
        
        # --- Inventaire et Ressources ---
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
        # --- Zone de Draft ---
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
                
                desc_y = rect_image.bottom + 10
                for ligne in lines:
                    self._dessiner_texte(self.ecran, ligne, (rect_carte.left + 8, desc_y), self.police_m, COULEUR_TEXTE)
                    desc_y += 20
                
                hint_rect = pygame.Rect(rect_carte.left, rect_carte.bottom - 25, rect_carte.width, 20)
                self._dessiner_texte(self.ecran, f"PRESSEZ [{i+1}]", hint_rect.center, self.police_p, COULEUR_ACCENT, ancre="center")

        if self.boite_message:
            self._dessiner_boîte_message()  
def _dessiner_boîte_message(self):
        overlay = pygame.Surface((FENETRE_L, FENETRE_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.ecran.blit(overlay, (0, 0))

        titre, texte = self.boite_message
        boite_l, boite_h = 400, 200
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

def _gérer_sélection_salle_draft(self, index):
        if index >= len(self.propositions):
            return
        
        y, x = self.cible
        salle_choisie = self.propositions[index]

        if not self.joueur.se_déplacer():
            self.boite_message = ("Déplacement Impossible", "Plus de pas restants pour poser la pièce!")
            self.action = None; return

        if salle_choisie.type_salle == "special" and not self.joueur.payer("coins", 3):
            self.boite_message = ("Pièce Spéciale", "Pas assez de Pièces (Coût: 3 Pièce). Annulation du placement.")
            self.joueur.pas_restants += 1
            self.action = None; return

        if salle_choisie.frais_entrée > 0:
            if not self.joueur.payer("coins", salle_choisie.frais_entrée):
                self.boite_message = ("Salle Payante", f"Besoin de {salle_choisie.frais_entrée} pièces pour entrer. Placement annulé.")
                self.joueur.pas_restants += 1
                self.action = None; return

        self.donjon[y][x] = salle_choisie
        self.joueur.pos_y, self.joueur.pos_x = y, x

        gagne = self.joueur.collecter(salle_choisie)
        if gagne:
            self._définir_dernier_butin(gagne)
            self.boite_message = ("Collecté", f"Vous avez trouvé : {gagne}")

        self.action = None
        self.cible = None
        self.propositions = []
        self.direction_selectionnee = None   