# objets.py


# Clés utilisées pour l'inventaire et les checks d'outils
PERMANENT_ITEMS = {
    "Shovel": "Pelle",              # Permet de creuser les 'endroits où creuser'
    "Hammer": "Marteau",            # Ouvre les coffres sans clé
    "LockpickKit": "Kit de Crochetage", # Ouvre les portes verrouillées
    "MetalDetector": "Détecteur de Métaux", # Augmente les chances de trouver clés et pièces
    "RabbitFoot": "Patte de Lapin", # Augmente les chances de trouver des objets rares
}

# La pool d'outils disponibles (utilisée dans la génération de salle)
# J'ai mis "Hammer" et "LockpickKit" 
POOL_OUTILS = list(PERMANENT_ITEMS.keys()) + ["Crowbar", "Torch", "Rope", "Goggles"] 


# Clés: Nom de l'objet, Valeurs: (Pas récupérés, Chance de spawn en % dans les salles standard)
CONSOMMABLES_PAS = {
    "pomme": (2, 0.25),      #  redonne 2 pas
    "Banane": (3, 0.20),     #  redonne 3 pas
    "Cake": (10, 0.05),      #  redonne 10 pas
    "Sandwich": (15, 0.03),  #  redonne 15 pas
    "repas": (25, 0.01),      #  redonne 25 pas
}

# Liste des noms d'objets (pour le butin)
ALL_LOOT_ITEMS = list(CONSOMMABLES_PAS.keys()) + ["coins", "gems", "keys", "dice"]


# Butin potentiel des éléments interactifs
COFFRE_LOOT = ["coins", "coins", "coins", "gems", "keys", "pomme", "Banane", "Hammer"]
CREUSER_LOOT = ["pomme", "coins", "coins", "Nothing", "Shovel"] # 'Nothing' = aucun butin
CASIER_LOOT = ["keys", "keys", "coins", "coins", "Banana", "LockpickKit"]