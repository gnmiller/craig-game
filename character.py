import item
import math


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

    #  Agility Code
    @property
    def agility(self) -> int:
        return self._agility

    @agility.setter
    def agility(self, val: int) -> None:
        self._agility = val
    #  Intellect Code

    @property
    def intellect(self) -> int:
        return self._intellect

    @intellect.setter
    def intellect(self, val: int) -> None:
        self._intellect = val

    # Charisma Code
    @property
    def charisma(self) -> int:
        return self._charisma

    @charisma.setter
    def charisma(self, val: int) -> None:
        self._charisma = val

    #  Constitution Code
    @property
    def constitution(self) -> int:
        return self._constitution

    @constitution.setter
    def constitution(self, val: int) -> None:
        self._constitution = val

    #  Luck Code
    @property
    def luck(self) -> int:
        return self._luck

    @luck.setter
    def luck(self, val: int) -> None:
        self._luck = val

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

    def __eq__(self, other):
        if isinstance(other, Stats):
            return self.strength == other.strength and \
                self.agility == other.agility and \
                self.intellect == other.intellect and \
                self.charisma == other.charisma and \
                self.constitution == other.constitution and \
                self.luck == other.luck
        return False


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

    def __eq__(self, other):
        if not isinstance(other, Gear):
            return False
        return (self.head == other.head and
                self.chest == other.chest and
                self.arms == other.arms and
                self.legs == other.legs and
                self.hands == other.hands and
                self.rings == other.rings and
                self.trinket == other.trinket and
                self.weapon == other.weapon and
                self.oh == other.oh)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.rings == []:
            ring_str = None
        else:
            ring_str = f"L: {self.rings[0]} ; R: {self.rings[1]}"
        return f"Head: {self.head}\n" \
            f"Chest: {self.chest}\n" \
            f"Arms: {self.arms}\n" \
            f"Legs: {self.legs}\n" \
            f"Hands: {self.hands}\n" \
            f"Rings: {ring_str}\n" \
            f"Trinket: {self.trinket}\n" \
            f"Weapon: {self.weapon}\n" \
            f"Off-hand: {self.oh}" \



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

    def __eq__(self, other=None) -> bool:
        if not isinstance(other, Level):
            return False
        return self.cur_level == other.cur_level


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

    def __eq__(self, other=None) -> bool:
        if not isinstance(other, Health):
            return False
        return self.cur_hp == other.cur_hp and \
            self.base_hp == other.base_hp

    def __ne__(self, other=None) -> None:
        return not self.__eq__(other)


class bt_Class:
    def __init__(self, name: str = None, stats: Stats = Stats()):
        self.name = name
        self.stats = stats
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
                raise TypeError("Invalid class choice!")

    @property
    def main_stat(self):
        return self.stats.strength

    @property
    def def_stats(self):
        return Stats()

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

    def __eq__(self, other):
        if isinstance(other, bt_Class):
            return self.name == other.name and self.stats == other.stats
        return False


class Warrior(bt_Class):
    def __init__(self):
        self.name = "warrior"
        base_stats = self.def_stats
        super(Warrior, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.strength

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.strength)
        return ret

    @property
    def def_stats(self):
        return Stats(strength=3, agility=1, intellect=1,
                     charisma=1, con=1, luck=1)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "sword" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Rogue(bt_Class):
    def __init__(self):
        self.name = "rogue"
        base_stats = self.def_stats
        super(Rogue, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.agility

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.agility)
        return ret

    @property
    def def_stats(self):
        return Stats(strength=1, agility=3, intellect=1,
                     charisma=1, con=1, luck=1)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "bow" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Wizard(bt_Class):
    def __init__(self):
        self.name = "wizard"
        base_stats = self.def_stats
        super(Wizard, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.intellect

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.intellect)
        return ret

    @property
    def def_stats(self):
        return Stats(strength=1, agility=1, intellect=3,
                     charisma=1, con=1, luck=1)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "staff" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Trader(bt_Class):
    def __init__(self):
        self.name = "trader"
        base_stats = self.def_stats
        super(Trader, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.charisma

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.charisma)
        return ret

    @property
    def def_stats(self):
        return Stats(strength=1, agility=1, intellect=1,
                     charisma=3, con=1, luck=1)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "axe" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Paladin(bt_Class):
    def __init__(self):
        self.name = "paladin"
        base_stats = self.def_stats
        super(Paladin, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.constitution

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.constitution)
        return ret

    @property
    def def_stats(self):
        return Stats(strength=1, agility=1, intellect=1,
                     charisma=1, con=3, luck=1)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        # if isinstance(g.weapon, item.Mace):
        if "mace" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Villager(bt_Class):
    def __init__(self):
        """The constructor initialized the object with the class name 'villager' and
            sets the base stats using `def_stas`"""
        self.name = "villager"
        base_stats = self.def_stats
        super(Villager, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.luck

    def get_gear_stats(self, g: Gear = Gear()):
        """Takes a `character.Gear` object as an argument and returns a list of
            luck stats from each in the Gear object."""
        ret = []
        for i in g:
            ret.append(i.luck)
        return ret

    @property
    def def_stats(self):
        """Returns a `character.Stats` object with the class' default stats.
            IE Strength: 1, Agility: 1, Intellect: 1, Charisma: 1, Con: 1, Luck: 3"""
        return Stats(strength=1, agility=1, intellect=1,
                     charisma=1, con=1, luck=3)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        """Takes a `character.Gear` object as an argument adn returns a float
            If the weapon name in the Gear object is pan the value is 1.1
            otherwise the value is 1.0"""
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
                 gear_block: Gear = Gear(),
                 class_choice: bt_Class = bt_Class('warrior')):
        self._level = level
        self._name = name
        self._gear = gear_block
        self._bt_class = class_choice
        self.hp = Health(self._bt_class.stats.constitution*10)
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
        return self._bt_class.stats

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

    #  character.Character internal/inherited funcs #

    def __str__(self) -> str:
        """Return a string of character data.

        Returns a string containing the name, level, health, and stats for the character"""
        stat_str = f"Strength \N{flexed biceps}: {self._bt_class.stats.strength}\n"\
                   f"Agility \N{athletic shoe}: {self._bt_class.stats.agility}\n"\
                   f"Intellect \N{brain}: {self._bt_class.stats.intellect}\n"\
                   f"Charisma \N{high voltage sign}: {self._bt_class.stats.intellect}\n"\
                   f"Constitution \N{bear face}: {self._bt_class.stats.charisma}\n"\
                   f"Luck \N{shamrock}: {self._bt_class.stats.luck}\n"

        # \u2764\ufe0f is red heart emoji
        return f"```Character: {self._name}\n" \
               f"Class: {self._bt_class}\n"\
               f"Health \u2764\ufe0f: {self.hp}\n"\
               f"Level: {self._level}\n" \
               f"Stats\n------\n{stat_str}\n```"

    def __eq__(self, other) -> bool:
        if isinstance(other, Character):
            return self.name == other.name and self.level == other.level \
                and self.gear == other.gear and self._bt_class == other._bt_class
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)
