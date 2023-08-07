import item
import math


import pdb


class Stats:
    """Wrapper for character stats.

    Attributes:
        strength        Character's strength
        agility         Character's agility
        intellect       Character's intellect
        charisma        Character's charisma
        constitution    Character's constitution
        luck            Character's luck
        inventory       The character's inventory (NYI)
    """
    def __init__(self, strength=0, agility=0, intellect=0,
                 charisma=0, con=0, luck=0) -> None:
        """Create a new stat block for a `character.Character`

        Parameters
        ----------
        strength    Starting strength value.
        agility    Starting agility value.
        intellect    Starting intellect value.
        charisma    Starting charisma value.
        constitution    Starting constitution value.
        luck    Starting luck value."""
        self._strength = strength
        self._agility = agility
        self._intellect = intellect
        self._charisma = charisma
        self._constitution = con
        self._luck = luck
        self._index = 0
        return

    #  Strength Code
    @property
    def strength(self) -> int:
        return self._strength

    @strength.setter
    def strength(self, val: int) -> None:
        self._strength = val

    @strength.deleter
    def strength(self) -> None:
        del self._strength
    #  End Strength

    #  Agility Code
    @property
    def agility(self) -> int:
        return self._agility

    @agility.setter
    def agility(self, val: int) -> None:
        self._agility = val

    @agility.deleter
    def agility(self) -> None:
        del self._agility
    #  End Agility

    #  Intellect Code
    @property
    def intellect(self) -> int:
        return self._intellect

    @intellect.setter
    def intellect(self, val: int) -> None:
        self._intellect = val

    @intellect.deleter
    def intellect(self) -> None:
        del self._intellect
    #  End Intellect

    # Charisma Code
    @property
    def charisma(self) -> int:
        return self._charisma

    @charisma.setter
    def charisma(self, val: int) -> None:
        self._charisma = val

    @charisma.deleter
    def charisma(self) -> None:
        del self._charisma
    #  End Charisma

    #  Constitution Code
    @property
    def constitution(self) -> int:
        return self._constitution

    @constitution.setter
    def constitution(self, val: int) -> None:
        self._constitution = val

    @constitution.deleter
    def constitution(self) -> None:
        del self._constitution
    #  End Constitution

    #  Luck Code
    @property
    def luck(self) -> int:
        return self._luck

    @luck.setter
    def luck(self, val: int) -> None:
        self._luck = val

    @luck.deleter
    def luck(self) -> None:
        del self._luck
    #  End Luck

    def __str__(self):
        """Generate a dict of stat_name: stat_value and return it as a string."""
        rstats = {}
        for k, v in vars(self).items():
            if "index" in k:
                continue
            rstats[k[1:len(k)]] = v
        return str(rstats)

    def __iter__(self):
        return self

    def __next__(self):
        """Iterate over the stats of this object.

        Iterates over vars(self). Using the data provided by vars()
        the iterator tries to lookup the key name (stat name), and
        then pulls the corresponding value from vars(). Meant to be
        scalable for new stats in the future.
        May have unexpected results if vars() does not provide a consistent
        ordering of the objects."""
        if self._index < len(vars(self).keys()):
            key = list(vars(self).keys())[self._index]
            if "index" in key:
                self._index += 1
                return next(self)
            value = vars(self)[key]
            self._index += 1
            return key[1:len(key)], value
        else:
            raise StopIteration


class Gear:
    """Container for a character's equipped items.

    This is effectively a container for `item.Equipment` objects. Each
    property is intended to hold a single `item.Equipment` with an
    `item.Slot` corresponding to the attribute name.

    Attributes:
        head Helmet equipment
        chest Chest armor
        arms Bracer/arm armor
        legs Leg armor
        hands Gloves
        rings A list of two rings.
        trinket A special trinket (ooo fancy)
        weapon A weapon
        oh Another weapon, or maybe a shield?
        """
    def __init__(self):
        """Create a new Gear container for a character.

        You start naked! No default values are assigned by the constructor.
        Except in the case of rings which is assigned an empty list."""
        self._head = None
        self._chest = None
        self._arms = None
        self._legs = None
        self._hands = None
        self._rings = []
        self._trinket = None
        self._weapon = None  # Main-hand weapon
        self._oh = None  # Off-hand weapon
        self._index = -1

    # Define the property getters and setters
    @property
    def head(self) -> item.Equipment:
        return self._head

    @head.setter
    def head(self, item: item.Equipment):
        self._head = item

    @property
    def chest(self):
        return self._chest

    @chest.setter
    def chest(self, item: item.Equipment):
        self._chest = item

    @property
    def arms(self) -> item.Equipment:
        return self._arms

    @arms.setter
    def arms(self, item: item.Equipment):
        self._arms = item

    @property
    def legs(self) -> item.Equipment:
        return self._legs

    @legs.setter
    def legs(self, item: item.Equipment):
        self._legs = item

    @property
    def hands(self) -> item.Equipment:
        return self._hands

    @hands.setter
    def hands(self, item: item.Equipment):
        self._hands = item

    @property
    def rings(self) -> item.Equipment:
        return self._rings

    @rings.setter
    def ring1(self, item: item.Equipment, rslot: int = 0):
        if rslot == 0 or rslot == 1:
            self._rings[rslot] = item
        else:
            raise ValueError("you can only wear 2 rings bozo")

    @property
    def trinket(self) -> item.Equipment:
        return self._trinket

    @trinket.setter
    def trinket(self, item: item.Equipment):
        self._trinket = item

    @property
    def weapon(self) -> item.Equipment:
        return self._weapon

    @weapon.setter
    def weapon(self, item: item.Equipment):
        self._weapon = item

    @property
    def oh(self) -> item.Equipment:
        return self._oh

    @oh.setter
    def oh(self, item: item.Equipment):
        self._oh = item

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        match self._index:
            case 0:
                return self.head
            case 1:
                return self.chest
            case 2:
                return self.arms
            case 3:
                return self.legs
            case 4:
                return self.hands
            case 5:
                if len(self._rings) <= 0:
                    return None
                return self._rings[0]
            case 6:
                if len(self._rings) <= 0:
                    return None
                return self._rings[1]
            case 7:
                return self.trinket
            case 8:
                return self.weapon
            case 9:
                return self.oh
            case _:
                raise StopIteration


class Level:
    """A container representing a character's level.

    An object containing the character's current level
    and experience amount.

    Attributes:
        cur_level   The character's current level as an integer
        exp         The character's experience count as an integer
    """
    def __init__(self, cur_level: int = 0, exp: int = 0):
        """Create a new Level object for a character.

        Characters start at level 0 with 0 experience by default.

        Parameters
        ----------
            cur_level   The character's current level
            exp         The character's current experience amount"""
        self._cur_level = cur_level
        self._exp = exp

    def _get_next(self):
        """Returns the exp needed for the next level for this `character.Level"""
        t = 100
        b = .15
        x = self.cur_level
        y = t * (1 + b) ** x
        return math.ceil(y)

    @property
    def cur_level(self) -> int:
        return self._cur_level

    @cur_level.setter
    def cur_level(self, value: int):
        if isinstance(value, int) and value >= 1:
            self._cur_level = value
        else:
            raise ValueError("Current level must be an integer >= 1.")

    @property
    def exp(self) -> int:
        return self._exp

    @exp.setter
    def exp(self, value: int):
        if isinstance(value, int) and value >= 0:
            self._exp = value
        else:
            raise ValueError("Experience points (exp) must be non-negative.")

    @property
    def exp_to_level(self) -> int:
        return self._exp_to_level

    @exp_to_level.setter
    def exp_to_level(self, value: int):
        if isinstance(value, int) and value > 0:
            self._exp_to_level = value
        else:
            raise ValueError("Exp to level must be a positive integer > 0.")

    def __str__(self) -> str:
        return str(self.cur_level)


class Health:
    def __init__(self, con_hp: int = 100, base_hp: int = 100):
        self.base_hp = base_hp
        self.max_hp = con_hp + self.base_hp
        self.cur_hp = self.max_hp

    @property
    def hp(self) -> int:
        return (self.cur_hp, self.max_hp)

    @hp.setter
    def hp(self, change: int = 0) -> int:
        self.cur_hp += change
        return self.cur_hp

    def recalc_hp(self, s: Stats = None):
        """Recalculate the max and current HP given a new stat block.

        Current HP is set as the percentage of the new max HP."""
        if not isinstance(s, Stats):
            raise TypeError("Stats object not passed to recalc_hp")
        else:
            pct_hp = self.cur_hp/self.max_hp
            self.max_hp = self.base_hp + s.constitution*10
            self.cur_hp = int(self.max_hp * pct_hp)
            return (self.cur_hp, self.max_hp)

    def __str__(self):
        return f"{self.cur_hp} / {self.max_hp}"


class bt_Class:
    def __init__(self, name: str = None):
        self.name = name
        self.stats = Stats()
        match name:
            case 'warrior':
                return
            case 'rogue':
                return
            case 'wizard':
                return
            case 'trader':
                return
            case 'paladin':
                return
            case 'villager':
                return
            case _:
                return

    @property
    def main_stat(self):
        return self.stats.strength

    def get_gear_stats(self, g: Gear = Gear()) -> []:
        ret = []
        for i in g:
            if i is None:
                continue
            ret.append(i.strength)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "sword" in g.weapon.name:
            return 1.1
        else:
            return 1.0

    def __str__(self):
        return self.name


class Warrior(bt_Class):
    def __init__(self):
        super.__init__()
        self.name = "warrior"
        return

    @property
    def main_stat(self):
        return self.stats.strength

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.strength)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "sword" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Rogue(bt_Class):
    def __init__(self):
        super.__init__()
        self.name = "rogue"
        return

    @property
    def main_stat(self):
        return self.stats.agility

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.agility)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "bow" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Wizard(bt_Class):
    def __init__(self):
        self.name = "wizard"
        return

    @property
    def main_stat(self):
        return self.stats.intellect

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.intellect)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "staff" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Trader(bt_Class):
    def __init__(self):
        super.__init__()
        self.name = "trader"
        return

    @property
    def main_stat(self):
        return self.stats.charisma

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.charisma)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "axe" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Paladin(bt_Class):
    def __init__(self):
        super.__init__()
        self.name = "paladin"
        return

    @property
    def main_stat(self):
        return self.stats.constitution

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.constitution)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        # if isinstance(g.weapon, item.Mace):
        if "mace" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Villager(bt_Class):
    def __init__(self):
        super.__init__()
        self.name = "villager"
        return

    @property
    def main_stat(self):
        return self.stats.luck

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.luck)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "pan" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Character:
    """The hero of the story! Contains all the important information.

    The Character class is designed to gather up all the other important
    information into one easy to reference location. The inention is to be
    able to snag all the information out of the DB create a `character.Gear`
    and a `character.Stat` then hand it all off to this object's constructor.

    Attributes:
        name        Who are you?
        level       `character.Level` for this character
        stats       `character.Stats` for this character
        gear        `Character.Gear` for this character
        bt_class    class (NYI)
        """
    def __init__(self, name: str,
                 level: Level = Level(0, 0),
                 stat_block: Stats = Stats(),
                 gear_block: Gear = Gear(),
                 bt_class: bt_Class = bt_Class()):
        self._level = level
        self._name = name
        self._stats = stat_block
        self._gear = gear_block
        self._bt_class = bt_class
        self.hp = Health(stat_block.constitution*10)
        return

    #  Level
    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value):
        if isinstance(value, int) and value > 0:
            self._level = value
        else:
            raise ValueError("Level must be a positive integer.")
    #  End Level

    #  Name
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str):
            self._name = value
        else:
            raise ValueError("Name must be a string.")
    #  End Name

    #  Stats
    @property
    def stats(self) -> Stats:
        return self._stats

    @stats.setter
    def stats(self, value: Stats):
        if isinstance(value, Stats):
            if self._stats.constitution != value.constitution:
                self.hp.recalc_hp(value)
            self._bt_class.stats = value
        else:
            raise ValueError("Stats must be a Stats.")
    #  End Stats

    #  Gear
    @property
    def gear(self) -> Gear:
        return self._gear

    @gear.setter
    def gear(self, value: Gear):
        if isinstance(value, Gear):
            self._gear = value
        else:
            raise ValueError("Gear must be a Gear.")
    #  End Gear

    # ATK & DEF
    @property
    def attack(self) -> int:
        base = 10
        # (10 + (main_stat + gear_stats) * .5)
        main_stat = self._bt_class.main_stat
        gear_stats = self._bt_class.get_gear_stats(self.gear)
        attack = 0
        if self.gear.weapon is not None:
            bonus = self._bt_class.attack_bonus(self.gear)
        else:
            bonus = 1.0
        for g in gear_stats:
            attack += g
        return int((base + (main_stat + attack) * .5)) * bonus

    @property
    def defense(self) -> int:
        base = 8
        main_stat = self._bt_class.main_stat
        gear_stats = self._bt_class.get_gear_stats(self.gear)
        defense = 0
        for g in gear_stats:
            defense += g
        return (base + (main_stat + defense) * .15)

    def __str__(self) -> str:
        return f"Character: {self._name}\n" \
               f"Class: {self._bt_class}\n"\
               f"Health: {self.hp}\n"\
               f"Level: {self._level}\n" \
               f"Stats: {self._bt_class.stats}"
