class Joueur:
    def __init__(self, pas_départ: int):
        self.pas_restants = pas_départ
        self.inventaire = {"steps": 0, "coins": 5, "gems": 1, "keys": 2, "dice": 3}
        self.ceinture_outils = ["Shovel", "Metal Detector"]
        self.pos_y = 8
        self.pos_x = 2

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
        for k in ("steps", "coins", "gems", "keys", "dice"):
            v = salle.ressources.get(k, 0)
            if v != 0:
                nouveau = self.inventaire.get(k, 0) + v
                if nouveau < 0:
                    nouveau = 0
                self.inventaire[k] = nouveau
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

        # 🔥 Effet spécial WEIGHT ROOM : divise les pas restants par 2
        if salle.nom.upper() == "WEIGHT ROOM":
            self.pas_restants = self.pas_restants // 2

        salle.visitee = True
        return gagne



# 2)  Génération de Donjon 

def _obtenir_direction_opposée(direction):
    opposites = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}
    return opposites.get(direction)


def obtenir_sorties_depuis_modele(nom_salle: str) -> dict:
    modele = DEFAULT_EXITS.get(nom_salle.upper(), {"haut": 1, "bas": 1, "gauche": 1, "droite": 1})
    return {d: bool(v) for d, v in modele.items()}


def générer_salle_aléatoire(y, x):
    global PIECES_DISPONIBLES

    if not PIECES_DISPONIBLES:
        # Si la pioche est vide, retourne une salle standard par défaut 
        return Chambre(x, y, nom="DEPOT",
                       sorties={"haut": 1, "bas": 1, "gauche": 1, "droite": 1},
                       frais_entrée=0)

    # Application de la rareté
    noms_disponibles = list(PIECES_DISPONIBLES)
    poids_tirage = []
    for nom in noms_disponibles:
        rareté = CARTOGRAPHIE_RARETE.get(nom.upper(), 0)
        poids = 1.0 / (3.0 ** rareté)
        poids_tirage.append(poids)

    if sum(poids_tirage) == 0:
        nom = random.choice(noms_disponibles)
    else:
        nom = random.choices(noms_disponibles, weights=poids_tirage, k=1)[0]

    # ...
    # Détermination si la salle est spéciale
    est_spéciale = nom.upper() in PIÈCES_SPÉCIALES_DÉFINIES
    type_salle = "special" if est_spéciale else "standard"
    sorties = obtenir_sorties_depuis_modele(nom)

    # Ressources de base (avec steps à la place de bread)
    base = {
        "steps": 0,
        "dice": 0,
        "coins": 0,
        "gems": 0,
        "keys": 0,
        "tools": []
    }

    if est_spéciale:
        base["gems"] = random.randint(1, 2)
        base["keys"] = random.randint(0, 1)

    # Chance générique d'avoir des outils
    chance_outil = 0.15 if est_spéciale else 0.10
    if random.random() < chance_outil and POOL_OUTILS:
        n_outils = 2 if (est_spéciale and random.random() < 0.25) else 1
        n_outils = min(n_outils, len(POOL_OUTILS))
        base["tools"] = random.sample(POOL_OUTILS, k=n_outils)

    # Helper pour garantir un certain nombre d'outils dans la salle
    def ajouter_outils(nb_voulu: int):
        nb_voulu = max(0, nb_voulu)
        deja = len(base["tools"])
        if nb_voulu <= deja:
            return
        candidats = [t for t in POOL_OUTILS if t not in base["tools"]]
        if not candidats:
            return
        nb_a_ajouter = min(nb_voulu - deja, len(candidats))
        nouveaux = random.sample(candidats, k=nb_a_ajouter)
        base["tools"].extend(nouveaux)

    # Effets spécifiques des salles 
    if nom == "BEDROOM":
        base["steps"] += 2
    elif nom == "DEN":
        base["gems"] += 1
    elif nom == "GUEST BEDROOM":
        base["steps"] += 10
    elif nom == "NOOK":
        base["keys"] += 1
    elif nom == "STOREROOM":
        base["keys"] += 1
        base["gems"] += 1
        base["coins"] += 1
    elif nom == "ATTIC":
        # Beaucoup d'outils (max possible)
        ajouter_outils(8)
    elif nom == "CHAPEL":
        # On perd 1 coin (si possible)
        base["coins"] -= 1
    elif nom == "CLOSET":
        ajouter_outils(2)
    elif nom == "GARAGE":
        base["keys"] += 3
    elif nom == "GYMNASIUM":
        base["steps"] -= 2
    elif nom == "MORNING ROOM":
        base["gems"] += 2
    elif nom == "RUMPUS ROOM":
        base["coins"] += 8
    elif nom == "TROPHY ROOM":
        base["gems"] += 8
    elif nom == "VAULT":
        base["coins"] += 40
    elif nom == "WALK IN CLOSET":
        ajouter_outils(4)
    elif nom == "WINE CELLAR":
        base["gems"] += 3
    elif nom == "BALLROOM":
        base["gems"] += 2
    elif nom == "NURSERY":
        base["steps"] += 5
    elif nom == "PANTRY":
        base["coins"] += 4
    #elif nom == "WEIGHT ROOM":
       # base["steps"] = base["steps"] // 2

    frais_entrée = 0
    if random.random() < (0.22 if est_spéciale else 0.15):
        frais_entrée = 1 if not est_spéciale else random.choice([1, 2, 3])

    return Chambre(x, y, type_salle=type_salle, ressources=base, sorties=sorties, nom=nom, frais_entrée=frais_entrée)


def générer_salle_compatible(y, x, direction_depuis_joueur: str):
    sortie_requise = _obtenir_direction_opposée(direction_depuis_joueur)
    salle_compatible = None

    while salle_compatible is None:
        salle_temp = générer_salle_aléatoire(y, x)

        if salle_temp.nom.upper() == "HALLWAY" and (x == 0 or x == 4 or y == 0 or y == 8):
            continue

        if salle_temp.sorties.get(sortie_requise, False):
            salle_compatible = salle_temp

    return salle_compatible


def générer_propositions_uniques(y, x, direction_depuis_joueur: str, compte=3):
    vu = set()
    props = []
    essais = 0
    max_essais = 80
    while len(props) < compte and essais < max_essais:
        r = générer_salle_compatible(y, x, direction_depuis_joueur)
        if r.nom.upper() not in vu:
            vu.add(r.nom.upper())
            props.append(r)
        essais += 1
    return props


def configurer_donjon(lignes=9, colonnes=6):
    grille = [[None for _ in range(colonnes)] for _ in range(lignes)]
    sorties_départ = obtenir_sorties_depuis_modele("ENTRANCE HALL")
    départ = Chambre(
        2,
        8,
        "standard",
        ressources={"steps": 1, "coins": 1, "gems": 0, "keys": 0, "dice": 1, "tools": []},
        sorties=sorties_départ,
        nom="ENTRANCE HALL",
        frais_entrée=0,
    )
    départ.visitee = True
    grille[8][2] = départ

    try:
        PIECES_DISPONIBLES.remove("ENTRANCE HALL")
    except ValueError:
        pass

    sorties_fin = obtenir_sorties_depuis_modele("ANTECHAMBER")
    fin = Chambre(
        2,
        0,
        "special",
        ressources={"steps": 3, "coins": 5, "gems": 5, "keys": 2, "dice": 3, "tools": []},
        sorties=sorties_fin,
        nom="ANTECHAMBER",
        frais_entrée=0,
    )
    grille[0][2] = fin

    try:
        PIECES_DISPONIBLES.remove("ANTECHAMBER")
    except ValueError:
        pass

    return grille