
import pygame
import sys
import os 
import random
from dossier_chambres import DOSSIER_IMAGE , CHEMIN_IMAGE_FOND , CHEMIN_IMAGE_INTRO , CARTOGRAPHIE_IMAGES_SALLES
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


# 2) Fonctions de Génération de Donjon (Globales)


def _obtenir_direction_opposée(direction):
    opposites = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}
    return opposites.get(direction)

def obtenir_sorties_depuis_modele(nom_salle: str) -> dict:
    modele = DEFAULT_EXITS.get(nom_salle.upper(), {"haut": 1, "bas": 1, "gauche": 1, "droite": 1})
    return {d: bool(v) for d, v in modele.items()}

def générer_salle_aléatoire(y, x):
    global PIECES_DISPONIBLES
    
    if not PIECES_DISPONIBLES:
        # Si la pioche est vide, retourne une salle standard par défaut (ou gère la fin du jeu)
        return Chambre(x, y, nom="DEPOT", sorties={"haut": 1, "bas": 1, "gauche": 1, "droite": 1}, frais_entrée=0)

    # --- Règle 1: Application de la rareté ---
    # Calcule les poids de chaque salle
    noms_disponibles = list(PIECES_DISPONIBLES)
    poids_tirage = []
    
    for nom in noms_disponibles:
        rareté = CARTOGRAPHIE_RARETE.get(nom.upper(), 0)
        poids = 1.0 / (3.0 ** rareté) # 1 / 3^rareté
        poids_tirage.append(poids)
        
    # S'assure qu'il reste au moins une salle à choisir
    if sum(poids_tirage) == 0:
        # Cas extrême où toutes les salles restantes auraient une rareté infinie (non possible ici, mais sécurité)
        nom = random.choice(noms_disponibles)
    else:
        # Sélectionne une salle pondérée par la rareté
        nom = random.choices(noms_disponibles, weights=poids_tirage, k=1)[0]
    # ------------------------------------------

    # Crée la salle (le retrait de la pioche se fera uniquement si la salle est choisie par le joueur)
    est_spéciale = random.random() < 0.3
    type_salle = "special" if est_spéciale else "standard"
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

    # Ajustement des ressources spécifiques à la salle (non modifiées)
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
    
    # Règle 3: Condition de placement (implémentation de base: doit avoir la sortie requise)
    while salle_compatible is None:
        salle_temp = générer_salle_aléatoire(y, x)
        
        # Le nom de la salle temporaire est toujours dans PIECES_DISPONIBLES à ce stade.
        
        # Conditions de placement personnalisées (Exemple: Hallway/Passage doit être central)
        if salle_temp.nom.upper() == "HALLWAY" and (x == 0 or x == 4 or y == 0 or y == 8):
             continue # Ne permet pas les Hallways aux extrémités (ajustez selon vos règles)

        # Condition de compatibilité de sortie
        if salle_temp.sorties.get(sortie_requise, False):
            salle_compatible = salle_temp
            
    return salle_compatible

def générer_propositions_uniques(y, x, direction_depuis_joueur: str, compte=3):
    vu = set(); props = []; essais = 0; max_essais = 80
    while len(props) < compte and essais < max_essais:
        # gère la rareté et les contraintes de placement
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
    
    # Retirer les pièces de départ/fin de la pioche (même si déjà exclus via la liste PIECES_DISPONIBLES)
    try:
        PIECES_DISPONIBLES.remove("ENTRANCE HALL")
    except ValueError:
        pass
    
    sorties_fin = obtenir_sorties_depuis_modele("ANTECHAMBER")
    fin = Chambre(2, 0, "special",
                ressources={"bread": 3, "coins": 5, "gems": 5, "keys": 2, "dice": 3, "tools": []},
                sorties=sorties_fin, nom="ANTECHAMBER", frais_entrée=0)
    grille[0][2] = fin
    
    try:
        PIECES_DISPONIBLES.remove("ANTECHAMBER")
    except ValueError:
        pass
        
    return grille