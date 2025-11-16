import os
# définir les portes de CHAQUE pièce.
# 1 pour une porte ouverte et 0 pour une porte fermée.
# Vous pourrez les modifier manuellement après avoir placé ce fichier.


DEFAULT_EXITS = { 
    # Convention : "haut", "bas", "gauche", "droite"
    
    # Pièces bleues (typiquement spéciales)
    "THE FOUNDATION": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "ENTRANCE HALL": {"haut": 1, "bas": 0, "gauche": 1, "droite": 1}, 
    "SPARE ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "ROTUNDA": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "PARLOR": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "BILLIARD ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "GALLERY": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "ROOM8": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "CLOSET": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "WALK IN CLOSET":{"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "ATTIC": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "STOREROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "NOOK": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "GARAGE": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "MUSIC ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "LOCKER ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "DEN": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "WINE CELLAR": {"haut": 0, "bas": 0, "gauche": 0, "droite": 0},
    "TROPHY ROOM": {"haut": 0, "bas": 0, "gauche": 0, "droite": 0},
    "BALLROOM": {"haut": 0, "bas": 0, "gauche": 0, "droite": 0},
    "PANTRY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "RUMPUS ROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "VAULT": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "OFFICE": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "DRAWING ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "STUDY": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "LIBRARY": {"haut": 0, "bas": 0, "gauche": 1, "droite": 1},
    "CHAMBER OF MIRRORS": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "THE POOL": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1}, 
    "DRAFTING STUDIO": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "UTILITY CLOSET": {"haut": 1, "bas": 0, "gauche": 1, "droite": 1},
    "BOILER ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1}, 
    "PUMP ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "SECURITY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "WORKSHOP": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0}, 
    "LABORATORY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "SAUNA": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0}, 
    "COAT CHECK": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0}, 
    "MAIL ROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0}, 
    "FREEZER": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0}, 
    "DINNING ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "OBSERVATORY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "CONFERENCE ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "AQUARIUM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "ANTECHAMBER": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0}, 

    #pieces violettes
    "BEDROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "BOUDOIR": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "GUEST BEDROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "NURSERY": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "SERVANT'S QUARTERS": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "BUNK ROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "THE LADY CHIP'S CHAMBER": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "MASTER BEDROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    
    # pièces marrons
    "HALLWAY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1}, 
    "WEST WING HALL": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "EAST WING HALL": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "CORRIDOR": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0}, 
    "PASSAGE WAY": {"haut": 1, "bas": 1, "gauche": 1, "droite": 1}, 
    "SECRET PASSAGE":{"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "FOYER": {"haut": 1, "bas": 1, "gauche": 0, "droite": 1},
    "GREAT HALL": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
   
   
   #pieces vertes
   "TERRACE": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
   "PATIO": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
   "COURTYARD": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
   "CLOISTER": {"haut": 1, "bas": 1, "gauche": 1, "droite": 1},
   "VERANDA": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
   "GREENHOUSE": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
   "MORNING ROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
   "SECRET GARDEN": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
   


   #pieces jaunes
    "COMMISSARY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "KITCHEN": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "LOCKSMITH": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "SHOWROOM": {"haut": 1, "bas": 1, "gauche": 0, "droite": 0},
    "LAUNDRY ROOM": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "BOOKSHOP": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "THE ARMORY": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "MOUNT HOLLY GIFT SHOP": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},




    #pieces rouges
    "LAVATORY": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},
    "CHAPEL": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "MAID'S CHAMBER": {"haut": 0, "bas": 1, "gauche": 1, "droite": 0},
    "ARCHIVES": {"haut": 1, "bas": 1, "gauche": 1, "droite": 1},
    "GYMNASIUM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "DARKROOM": {"haut": 0, "bas": 1, "gauche": 1, "droite": 1},
    "WEIGHT ROOM": {"haut": 1, "bas": 1, "gauche": 1, "droite": 1},
    "FURNACE": {"haut": 0, "bas": 1, "gauche": 0, "droite": 0},


    }

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