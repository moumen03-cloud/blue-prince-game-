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
        self.inventory = {"bread": 0, "coins": 5, "gems": 1, "keys": 2, "dice": 2}
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
    
    def collect(self, room):
        if room.visited:
            return {}
        gained = {}
        for k in ("bread", "coins", "gems", "keys", "dice"):
            v = room.resources.get(k, 0)
            if v > 0:
                self.inventory[k] = self.inventory.get(k, 0) + v
                gained[k] = v
                room.resources[k] = 0
        tools = room.resources.get("tools", [])
        if tools:
            gained["tools"] = []
            for t in tools:
                if t not in self.toolbelt:
                    self.toolbelt.append(t)
                gained["tools"].append(t)
            room.resources["tools"] = []
        room.visited = True
        return gained
        
ALL_ROOM_NAMES = [name for name in DEFAULT_EXITS.keys() if name not in {"ENTRANCE HALL", "ANTECHAMBER"}]
TOOL_POOL = ["Crowbar", "Lockpick", "Torch", "Rope", "Goggles"]

def _get_opposite_direction(direction):
    opposites = {"haut": "bas", "bas": "haut", "gauche": "droite", "droite": "gauche"}
    return opposites.get(direction)

def get_exits_from_template(room_name: str) -> dict:
    template = DEFAULT_EXITS.get(room_name.upper(), {"haut": 1, "bas": 1, "gauche": 1, "droite": 1})
    return {d: bool(v) for d, v in template.items()}

def generate_random_room(y, x):
    is_special = random.random() < 0.3
    room_type = "special" if is_special else "standard"
    name = random.choice(ALL_ROOM_NAMES)
    exits = get_exits_from_template(name)

    base = {"bread": random.randint(0, 1),
            "dice": random.randint(0, 1),
            "coins": random.randint(0, 2),
            "gems": 0,
            "keys": 0,
            "tools": []}
    if is_special:
        base["gems"] = random.randint(1, 2)
        base["keys"] = random.randint(0, 1)

    if name == "BEDROOM":
        base["dice"] += 2
    elif name == "DEN":
        base["gems"] += 1
    elif name == "GUEST BEDROOM":
        base["bread"] += 10
    elif name == "NOOK":
        base["keys"] += 1
    elif name == "STOREROOM":
        base["keys"] += 1; base["gems"] += 1; base["coins"] += 1

    tool_chance = 0.15 if is_special else 0.10
    if random.random() < tool_chance:
        n_tools = 2 if (is_special and random.random() < 0.25) else 1
        base["tools"] = random.sample(TOOL_POOL, k=min(n_tools, len(TOOL_POOL)))

    entrance_fee = 0
    if random.random() < (0.22 if is_special else 0.15):
        entrance_fee = 1 if not is_special else random.choice([1, 2, 3])

    return Room(x, y, room_type=room_type, resources=base, exits=exits, name=name, entrance_fee=entrance_fee)

def generate_compatible_room(y, x, direction_from_player: str):
    required_exit = _get_opposite_direction(direction_from_player)
    compatible_room = None
    while compatible_room is None:
        temp_room = generate_random_room(y, x)
        if temp_room.exits.get(required_exit, False):
            compatible_room = temp_room
    return compatible_room

def generate_unique_proposals(y, x, direction_from_player: str, count=3):
    seen = set(); props = []; tries = 0; max_tries = 80
    while len(props) < count and tries < max_tries:
        r = generate_compatible_room(y, x, direction_from_player)
        if r.name.upper() not in seen:
            seen.add(r.name.upper()); props.append(r)
        tries += 1
    return props

def setup_dungeon(rows=9, cols=6):
    grid = [[None for _ in range(cols)] for _ in range(rows)]
    start_exits = get_exits_from_template("ENTRANCE HALL")
    start = Room(1, 8, "standard",
                 resources={"bread": 1, "coins": 1, "gems": 0, "keys": 0, "dice": 1, "tools": []},
                 exits=start_exits, name="ENTRANCE HALL", entrance_fee=0)
    start.visited = True
    grid[8][1] = start
    end_exits = get_exits_from_template("ANTECHAMBER")
    end = Room(2, 0, "special",
               resources={"bread": 3, "coins": 5, "gems": 5, "keys": 2, "dice": 3, "tools": []},
               exits=end_exits, name="ANTECHAMBER", entrance_fee=0)
    grid[0][2] = end
    return grid


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


    