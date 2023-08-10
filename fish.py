import random
import config
import item


class FishingPool:
    def __init__(self, name: str = "lake", fish: list = [], diff: int = 10):
        self._avail_fish = fish
        self._name = name
        self._difficulty = diff

    def go_fishing(self, luck: int = 0, fishing_rod: item.Equipment = None):
        caught = []
        # rod_bonus = 1.0
        luck_bonus = int(luck*0.1)
        min_caught = 1
        max_caught = max(luck_bonus, 2)
        for f in self._avail_fish:
            crit = config.crit(diff=self._difficulty, luck=luck)
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
