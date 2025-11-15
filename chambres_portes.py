import os

DEFAULT_EXITS = { 
   
    # Pièces bleues 
    "AQUARIUM": {"haut": 1, "bas": 0, "gauche": 1, "droite": 1},
    "DEN": {"haut": 1, "bas": 1, "gauche": 1, "droite": 0},
    "WEST WING HALL": {"haut": 0, "bas": 0, "gauche": 1, "droite": 0}, 
    "DRAWING ROOM": {"haut": 1, "bas": 1, "gauche": 1, "droite": 0},
    "SOLARIUM": {"haut": 1, "bas": 0, "gauche": 0, "droite": 0},
    "CONFERENCE ROOM": {"haut": 1, "bas": 1, "gauche": 1, "droite": 0},
    "NOOK": {"haut": 0, "bas": 0, "gauche": 1, "droite": 0},
    "PARLOR": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "THE POOL": {"haut": 1, "bas": 1, "gauche": 1, "droite": 0}, 
    "RUMPUS ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "SPARE ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "STUDY": {"haut": 0, "bas": 0, "gauche": 0, "droite": 1},
    "WALK-IN CLOSET": {"haut": 0, "bas": 0, "gauche": 0, "droite": 1},
    "WORKSHOP": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},

    # Pièces marrons 
    "HALLWAY": {"haut": 1, "bas": 1, "gauche": 0, "droite": 1}, # Couloir vertical
    "CLOSET": {"haut": 0, "bas": 0, "gauche": 1, "droite": 0},
    "STOREROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "CORRIDOR": {"haut": 0, "bas": 0, "gauche": 1, "droite": 1}, # Couloir horizontal
    "BEDROOM": {"haut": 1, "bas": 0, "gauche": 0, "droite": 1},
    "CLOISTER": {"haut": 1, "bas": 1, "gauche": 1, "droite": 1},
    "COMMISSARY": {"haut": 0, "bas": 1, "gauche": 0, "droite": 1},
    "DINING ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 1},
    "FURNACE": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "GUEST BEDROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "GYMNASIUM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 1},
    "KITCHEN": {"haut": 1, "bas": 0, "gauche": 0, "droite": 1},
    "LAVATORY": {"haut": 0, "bas": 0, "gauche": 1, "droite": 0},
    "PANTRY": {"haut": 1, "bas": 0, "gauche": 0, "droite": 1},
    "PATIO": {"haut": 1, "bas": 0, "gauche": 1, "droite": 0},
    "SERVANT'S QUARTERS": {"haut": 0, "bas": 0, "gauche": 1, "droite": 0},
     "BOUDOIR": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    # Pièces spéciales (Point de départ / Objectif)
    "ENTRANCE HALL": {"haut": 1, "bas": 0, "gauche": 1, "droite": 1}, 
    "ANTECHAMBER": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0}, 
   
    }


IMAGE_FOLDER = "images projet"
BACKGROUND_IMAGE_PATH = os.path.join(IMAGE_FOLDER, "image arriere plan.png")

ROOM_IMAGES = {
    "ANTECHAMBER": os.path.join(IMAGE_FOLDER, "antechamber.png.png"),
    "AQUARIUM": os.path.join(IMAGE_FOLDER, "aquarium.png.png"),
    "BEDROOM": os.path.join(IMAGE_FOLDER, "bedroom.png.png"),
    "BOUDOIR": os.path.join(IMAGE_FOLDER, "boudoir.png"),
    "CLOISTER": os.path.join(IMAGE_FOLDER, "cloister.png.png"),
    "CLOSET": os.path.join(IMAGE_FOLDER, "closet.ong.png"),
    "COMMISSARY": os.path.join(IMAGE_FOLDER, "commissary.png.png"),
    "CONFERENCE ROOM": os.path.join(IMAGE_FOLDER, "conference room.png.png"),
    "CORRIDOR": os.path.join(IMAGE_FOLDER, "corridor.png.png"),
    "DEN": os.path.join(IMAGE_FOLDER, "den.png.png"),
    "DINING ROOM": os.path.join(IMAGE_FOLDER, "dining room.png.png"),
    "DRAWING ROOM": os.path.join(IMAGE_FOLDER, "drawing room.png.png"),
    "ENTRANCE HALL": os.path.join(IMAGE_FOLDER, "entrance hall.png.png"),
    "FURNACE": os.path.join(IMAGE_FOLDER, "furnace.png.png"),
    "GUEST BEDROOM": os.path.join(IMAGE_FOLDER, "guest room.png.png"),
    "GYMNASIUM": os.path.join(IMAGE_FOLDER, "gymnasium.png.png"),
    "HALLWAY": os.path.join(IMAGE_FOLDER, "hallway.png.png"),
    "KITCHEN": os.path.join(IMAGE_FOLDER, "kitchen.png.png"),
    "LAVATORY": os.path.join(IMAGE_FOLDER, "lvatory.png.png"),
    "NOOK": os.path.join(IMAGE_FOLDER, "nook.png.png"),
    "PANTRY": os.path.join(IMAGE_FOLDER, "pantry.png.png"),
    "PARLOR": os.path.join(IMAGE_FOLDER, "parlor.png.png"),
    "PATIO": os.path.join(IMAGE_FOLDER, "patio.png.png"),
    "THE POOL": os.path.join(IMAGE_FOLDER, "pool.png.png"),
    "RUMPUS ROOM": os.path.join(IMAGE_FOLDER, "rumpus room.png"),
    "SERVANT'S QUARTERS": os.path.join(IMAGE_FOLDER, "sevant's quarters.png.png"),
    "SOLARIUM": os.path.join(IMAGE_FOLDER, "solarium.png.png"),
    "SPARE ROOM": os.path.join(IMAGE_FOLDER, "spare room.png.png"),
    "STOREROOM": os.path.join(IMAGE_FOLDER, "storeroom.png.png"),
    "STUDY": os.path.join(IMAGE_FOLDER, "study.png.png"),
    "WALK-IN CLOSET": os.path.join(IMAGE_FOLDER, "walk in closet.png.png"),
    "WEST WING HALL": os.path.join(IMAGE_FOLDER, "west wing hall.png.png"),
    "WORKSHOP": os.path.join(IMAGE_FOLDER, "worksop.png.png"),
}