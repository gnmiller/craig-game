import random
import config
import item


class FishingPool:
    def __init__(self, name: str = "lake", fish: list = [], diff: int = 10,  min_level: int = 0):
        self.avail_fish = fish
        self.name = name
        self.difficulty = diff
        self.min_level = min_level

    def go_fishing(self, luck: int = 0, fishing_rod: item.Equipment = None):
        caught = []
        # rod_bonus = 1.0
        luck_bonus = int(luck*0.1)
        min_caught = 1
        max_caught = max(luck_bonus, 2)
        for f in self.avail_fish:
            crit = config.crit(diff=self.difficulty, luck=luck)
            if fishing_rod is not None:
                # get bonus from fishing rod
                pass
            num_caught = random.randint(min_caught, max_caught)
            if crit:
                num_caught *= 2
            for i in range(num_caught):
                caught.append(f)
        return caught


class Fish(item.Item):
    def __init__(self, name: str = "cod", value: int = 1):
        self.name = name
        self.value = value

    def __str__(self):
        return f"{self.name}, {self.value}"

    def __hash__(self):
        return hash((self.name, self.value))

    def __eq__(self, other):
        if not isinstance(other, Fish):
            return False
        if self.name == other.name and self.value == other.value:
            return True
        else:
            return False


def build_pool(name: str = 'pond', difficulty: int = 10, min_lvl: int = 0, avail_fish: list = [], fish_dict: dict = {}):
    if not isinstance(avail_fish, list):
        raise TypeError("provide me a list buddy")
    if not isinstance(fish_dict, dict):
        raise TypeError("provide me a dict buddy")
    out_list = []
    for k, v in fish_dict.items():
        if k in avail_fish:
            out_list.append(Fish(k, v))
    return FishingPool(name, out_list.copy(), difficulty, min_lvl)


fish_dict = {
    "Salmon": 7,
    "Tuna": 10,
    "Cod": 3,
    "Trout": 5,
    "Bass": 3,
    "Catfish": 5,
    "Mahi Mahi": 25,
    "Snapper": 5,
    "Swordfish": 10,
    "Haddock": 5,
    "Grouper": 8,
    "Perch": 4,
    "Mackerel": 3,
    "Tilapia": 6,
    "Carp": 4,
    "Pike": 7,
    "Anchovy": 1,
    "Sardine": 1,
    "Flounder": 4,
    "Halibut": 5,
    "Bluegill": 1,
    "Walleye": 6
}
pond_fish = ['Cod', 'Bass', 'Bluegill']
river_fish = ['Bluegill', 'Bass', 'Catfish', 'Trout', 'Perch', 'Pike']
lake_fish = ['Bass', 'Catfish', 'Pike', 'Walleye', 'Perch', 'Carp', 'Sturgeon', 'Bluegill']
fishing_pools = []
fishing_pools.append(build_pool(name='pond',
                                difficulty=8,
                                avail_fish=pond_fish,
                                fish_dict=fish_dict,
                                min_lvl=0))
fishing_pools.append(build_pool(name='river',
                                difficulty=10,
                                avail_fish=river_fish,
                                fish_dict=fish_dict,
                                min_lvl=3))
fishing_pools.append(build_pool(name='lake',
                                difficulty=12,
                                avail_fish=lake_fish,
                                fish_dict=fish_dict,
                                min_lvl=5))
