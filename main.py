class Room:
    def __init__(self, x, y, room_type="standard", resources=None, exits=None, name="ROOM", entrance_fee=0):
        self.pos_x = x
        self.pos_y = y
        self.room_type = room_type
        self.cost = 1 if room_type == "special" else 0  # coût de pose (hérité)
        # [TOOLS] on ajoute "tools" (liste) dans les ressources
        self.resources = resources if resources is not None else {
            "bread": 0, "coins": 0, "gems": 0, "keys": 0, "dice": 0, "tools": []
        }
        self.exits = exits if exits is not None else {}
        self.visited = False
        self.name = name
        # [PAID] frais d’entrée (coins) à payer pour accéder/collecter
        self.entrance_fee = max(0, int(entrance_fee))
       
class Player:
    def __init__(self, start_steps: int):
        self.steps_left = start_steps
        self.inventory = {"bread": 0, "coins": 5, "gems": 1, "keys": 2, "dice": 3}
        self.toolbelt = ["Shovel", "Metal Detector"]
        self.pos_y = 8
        self.pos_x = 1

    def move(self):
        if self.steps_left > 0:
            self.steps_left -= 1
            return True
        return False

    def pay(self, item, amount):
        if self.inventory.get(item, 0) >= amount:
            self.inventory[item] -= amount
            return True
        return False    
        
