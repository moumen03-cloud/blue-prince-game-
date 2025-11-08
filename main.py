
class Room:
    def __init__(self, x, y, room_type="standard",exits=None, name="ROOM", ):
        self.pos_x = x
        self.pos_y = y
        self.room_type = room_type
        self.cost = 1 if room_type == "special" else 0  
        
        self.exits = exits if exits is not None else {}
        self.visited = False
        self.name = name
       
class Player:
    def __init__(self, start_steps: int):
        self.steps_left = start_steps
        self.inventory = {"bread": 0, "coins": 5, "gems": 1, "keys": 2, "dice": 3}
        self.toolbelt = ["Shovel", "Metal Detector"]
        self.pos_y = 8
        self.pos_x = 1
        
