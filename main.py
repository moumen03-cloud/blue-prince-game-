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
    "ANTECHAMBER": os.path.join(DOSSIER_IMAGE, "antechamber.png.png"),
    "AQUARIUM": os.path.join(DOSSIER_IMAGE, "aquarium.png.png"),
    "BEDROOM": os.path.join(DOSSIER_IMAGE, "bedroom.png.png"),
    "BOUDOIR": os.path.join(DOSSIER_IMAGE, "boudoir.png"),
    "CLOISTER": os.path.join(DOSSIER_IMAGE, "cloister.png.png"),
    "CLOSET": os.path.join(DOSSIER_IMAGE, "closet.ong.png"),
    "COMMISSARY": os.path.join(DOSSIER_IMAGE, "commissary.png.png"),
    "CONFERENCE ROOM": os.path.join(DOSSIER_IMAGE, "conference room.png.png"),
    "CORRIDOR": os.path.join(DOSSIER_IMAGE, "corridor.png.png"),
    "DEN": os.path.join(DOSSIER_IMAGE, "den.png.png"),
    "DINING ROOM": os.path.join(DOSSIER_IMAGE, "dining room.png.png"),
    "DRAWING ROOM": os.path.join(DOSSIER_IMAGE, "drawing room.png.png"),
    "ENTRANCE HALL": os.path.join(DOSSIER_IMAGE, "entrance hall.png.png"),
    "FURNACE": os.path.join(DOSSIER_IMAGE, "furnace.png.png"),
    "GUEST BEDROOM": os.path.join(DOSSIER_IMAGE, "guest room.png.png"),
    "GYMNASIUM": os.path.join(DOSSIER_IMAGE, "gymnasium.png.png"),
    "HALLWAY": os.path.join(DOSSIER_IMAGE, "hallway.png.png"),
    "KITCHEN": os.path.join(DOSSIER_IMAGE, "kitchen.png.png"),
    "LAVATORY": os.path.join(DOSSIER_IMAGE, "lvatory.png.png"),
    "NOOK": os.path.join(DOSSIER_IMAGE, "nook.png.png"),
    "PANTRY": os.path.join(DOSSIER_IMAGE, "pantry.png.png"),
    "PARLOR": os.path.join(DOSSIER_IMAGE, "parlor.png.png"),
    "PATIO": os.path.join(DOSSIER_IMAGE, "patio.png.png"),
    "THE POOL": os.path.join(DOSSIER_IMAGE, "pool.png.png"),
    "RUMPUS ROOM": os.path.join(DOSSIER_IMAGE, "rumpus room.png"),
    "SERVANT'S QUARTERS": os.path.join(DOSSIER_IMAGE, "sevant's quarters.png.png"),
    "SOLARIUM": os.path.join(DOSSIER_IMAGE, "solarium.png.png"),
    "SPARE ROOM": os.path.join(DOSSIER_IMAGE, "spare room.png.png"),
    "STOREROOM": os.path.join(DOSSIER_IMAGE, "storeroom.png.png"),
    "STUDY": os.path.join(DOSSIER_IMAGE, "study.png.png"),
    "WALK-IN CLOSET": os.path.join(DOSSIER_IMAGE, "walk in closet.png.png"),
    "WEST WING HALL": os.path.join(DOSSIER_IMAGE, "west wing hall.png.png"),
    "WORKSHOP": os.path.join(DOSSIER_IMAGE, "worksop.png.png"),
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