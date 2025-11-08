

# =========================
# 1) Modèles du jeu
# =========================



class Room:
    def __init__(self, x, y, room_type="standard",exits=None, name="ROOM", ):
        self.pos_x = x
        self.pos_y = y
        self.room_type = room_type
        self.cost = 1 if room_type == "special" else 0  
        
        self.exits = exits if exits is not None else {}
        self.visited = False
        self.name = name
        # [PAID] frais d’entrée (coins) à payer pour accéder/collecter
        #self.entrance_fee = max(0, int(entrance_fee))

        