import item
import math
from collections import Counter


class Stats:
    """
    Wrapper for character stats.

    Attributes
    ----------
    strength:       :type:`int`
        Character's strength
    agility:        :type:`int`
        Character's agility
    intellect:      :type:`int`
        Character's intellect
    charisma:      :type:`int`
        Character's charisma
    constitution:   :type:`int`
        Character's constitution
    luck:           :type:`int`
        Character's luck

    Methods
    -------
    None
    """

    def __init__(self, strength=0, agility=0, intellect=0,
                 charisma=0, con=0, luck=0) -> None:
        """
        Create a new stat block for a `character.Character`

        Parameters
        ----------
        strength:       int
            Starting strength value.
        agility:        int
            Starting agility value.
        intellect:      int
            Starting intellect value.
        charisma:       int
            Starting charisma value.
        constitution:   int
            Starting constitution value.
        luck:           int
            Starting luck value.
        """
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
        """
        Generate a dict of stat_name: stat_value and return it as a string.
        """
        rstats = {}
        for k, v in vars(self).items():
            if "index" in k:
                continue
            rstats[k[1:len(k)]] = v
        return str(rstats)

    def __iter__(self):
        return self

    def __next__(self):
        """
        Iterate over the stats of this object.

        Iterates over vars(self). Using the data provided by :func:`vars()`
        the iterator tries to lookup the key name (stat name), and
        then pulls the corresponding value from vars(). Meant to be
        scalable for new stats in the future.
        May have unexpected results if :func:`vars()` does not provide a
        consistent ordering of the objects.
        """
        if self._index < len(vars(self).keys()):
            key = list(vars(self).keys())[self._index]
            if "index" in key:
                self._index += 1
                return next(self)
            value = vars(self)[key]
            self._index += 1
            return key[1:len(key)], value
        else:
            self._index = 0
            raise StopIteration

    def __eq__(self, other):
        """
        Compare two :class:`Stats` objects for equality.

        Parameters
        ----------
        other:  :class:`Stats`
            The :class:`Stats` object to compare this on against.

        Returns
        -------
        True if both objects have the same attributes.
        False otherwise or an object that is not a `Stats` is passed.
        """
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

    This is effectively a container for :class:`item.Equipment` objects. Each
    property is intended to hold a single `item.Equipment` with an
    :class:`item.Slot` corresponding to the attribute name.

    Attributes
    ----------
    head:       :class:`item.Head`
        Helmet equipment
    chest:      :class:`item.Chest`
        Chest armor
    arms:       :class:`item.Arms`
        Bracer/arm armor
    legs:       :class:`item.Legs`
        Leg armor
    hands:      :class:`item.Hands`
        Gloves
    rings:      :type:`list`
        A list of two rings.
    trinket:    :class:`item.Trinket`
        A special trinket (ooo fancy)
    weapon:     :class:`item.Weapon`
        A weapon
    oh:         :class:`item.OffHand`
        Another weapon, or maybe a shield?

    Methods
    -------
    None
    """

    def __init__(self):
        """
        Create a new :class:`Gear` container for a character.

        You start naked! No default values are assigned by the constructor.
        Except in the case of rings which is assigned an empty list.
        """
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
                self._index = -1
                raise StopIteration

    def __eq__(self, other):
        """
        Compare two :class:`Gear` objects for equality.

        Checks each :class:`item.Item` in the :class:`character.Gear`
        individually for equality.

        Parameters
        ----------
        other:  :class:`Gear`
            Gear object to compare this one against.

        Returns
        -------
        True:
            If all items in the :class:`Gear` are equal per
            :func:`item.Equipment.__eq__()`
        False:
            If a non :class:`Gear` is passed as other or any 
        items in the container are not equal.
        """
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

    def __str__(self):
        """
        Return the string representation of the :class:`Gear`.

        Return a string representation of the :class:`Gear` object. Each
        :class:`item.Item` in the :class:`character.Gear` is evaluated
        individually.
        """
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
            f"Off-hand: {self.oh}"


class Level:
    """A container representing a character's level.

    An object containing the character's current level
    and experience amount.

    TODO ensure that current_experience cannot exceed max
    TODO ensure current level matches experience value

    Attributes
    ----------
    cur_level:  :type:`int`
        The character's current level as an integer
    exp:        :type:`int`
        The character's experience count as an integer

    Methods
    -------
    get_next():
        Returns the amount of experience needed to level up. This is the TOTAL
        amount required. Not the difference needed.
    check_next():
        Returns if current experience value if greater than get_next()
    """

    def __init__(self, cur_level: int = 0, exp: int = 0):
        """Create a new Level object for a character.

        Characters start at level 0 with 0 experience by default.

        Parameters
        ----------
        cur_level:  :type:`int`
            The character's current level
        exp:        :type:`int`
            The character's current experience amount"""
        self._cur_level = cur_level
        self._exp = exp

    def get_next(self):
        """
        Returns the exp needed for the next level for this 
        :class:`character.Level`.
        """
        t = 100
        b = .15
        x = self.cur_level
        y = t * (1 + b) ** x
        return math.ceil(y)

    def check_next(self):
        """Check if enough experience has been accrued to level up."""
        return self.exp > self.get_next()

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
        return self.get_next() - self.cur_exp

    @exp_to_level.setter
    def exp_to_level(self, value: int):
        if isinstance(value, int) and value > 0:
            self._exp_to_level = value
        else:
            raise ValueError("Exp to level must be a positive integer > 0.")

    def __str__(self) -> str:
        return str(self.cur_level)

    def __eq__(self, other=None) -> bool:
        """
        Compare two :class:`Level` objects for equality.

        Only checks if the level is equal. If experience values
        differ will still return True.

        TODO: Update this to check exp values too?

        Parameters
        ----------
        other:  :class:`Level`
            Level object to compare this one against.

        Returns
        -------
        True:
            If each :class:`Level` has the same cur_level attribute.
        False:
            If the cur_level's are different or a non-:class:`Level`
            is passed as other.
        """
        if not isinstance(other, Level):
            return False
        return self.cur_level == other.cur_level


class Health:
    """
    Contains the health information for a character.

    Attributes
    ----------
    hp: :type:`tuple`
        Contains current and max HP values for the character as a tuple
        (cur hp, max hp)

    Methods
    -------
    recalc_hp(s):
        Determine the correct value of max_hp and adjust cur_hp accordingly.
    """

    def __init__(self, con_hp: int = 100, base_hp: int = 90):
        """Create a new `character.Health` object with `con_hp` and `base_hp` values.

        Parameters
        ----------
        con_hp  How much HP the character is getting from Constitution (default 100)
        base_hp The base HP for the given class (default 100)"""
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
        """
        Recalculate the max and current HP given a new stat block.

        Current HP is set as the percentage of the new max HP. This would
        generally be used when leveling up a charcter or otherwise adjusting
        their constution (like when equipping gear with +CON).

        Parameters
        ----------
        s:  :class:`Stats`
            The new stat block to calculate HP based on

        Returns
        -------
        A :type:`tuple` containing the new HP values (cur, max)
        """
        if not isinstance(s, Stats):
            raise TypeError("Stats object not passed to recalc_hp")
        else:
            pct_hp = self.cur_hp/self.max_hp
            self.max_hp = self.base_hp + s.constitution*10
            self.cur_hp = int(self.max_hp * pct_hp)
            return (self.cur_hp, self.max_hp)

    def __str__(self):
        """
        Return a string with current hp / max hp (literal)
        """
        return f"{self.cur_hp} / {self.max_hp}"

    def __eq__(self, other=None) -> bool:
        """
        Compare two :class:`Health` objects for equality.

        Both current and max hp are checked for equality.
        Returns True if both are equal, otherwise returns
        false.

        Parameters
        ----------
        other:  :class:`Health`
            Health object to compare this one against.

        Returns
        -------
        True:
            If current and max HP values are the same for both objects.
        False:
            If either value differs or an invalid object is passed in as other.
        """
        if not isinstance(other, Health):
            return False
        return self.cur_hp == other.cur_hp and \
            self.base_hp == other.base_hp


class bt_Class:
    """
    Superclass for character classes. Inherited by each specific class.

    Generally not intended to be used on its own when making characters. Use
    the sub-classes instead as the default values for this class may not work
    properly with all application functionality.

    config.data['classes'] contains a list of available classes (as strings).

    Attributes
    ----------
    name:        :type:`str`
        The name of the class.
    stats:       :class:`Stats`
        A :class:`character.Stats` object with the classes stats.
    def_stats:  :class:`Stats`
        The default stat array for the class

    Methods
    -------
    get_gear_stats(g):
        Get the amount of bonus main stat provided by equipped
        :class:`item.Equipment`.
    attack_bonus(g):
        Get how much bonus attack damage is provided by equipped
        :class:`Gear`
    defense_bonus(g) -- NYI:
        Get how much bonus damage reduction is provided by equipped
        :class:`Gear`
    """

    def __init__(self, name: str = None, stats: Stats = Stats()):
        """
        Create a new bt_class object with its name as name and its stats as stats.

        Parameters
        ----------
        name    The name of the class to use. A list of current classes is
                    available in `config.data['classes']`

        stats   The `character.Stats` object for this character. If None is specified
                    the default constructor with all stats as 0 is called.
        """
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
        """The character's primary attribute."""
        return self.stats.strength

    @property
    def def_stats(self):
        """The default stat array for a class."""
        return Stats()

    def get_gear_stats(self, g: Gear = Gear()) -> []:
        """
        Return the bonuses for a classes main stat from gear.

        Since only main stat will (currently) affect anything we only
        check the classes 'main' stat.

        Parameters
        ----------
        g:  :class:`Gear`
            The gear object to extract stats from

        Returns
        -------
        :type:`list`:
            A list containing each gear slots bonus. Bonuses *should* be in
            the same ordering as the :var:`Item.Slot.slots` dict. This is not
            ensured however.
        """
        ret = []
        for i in g:
            if i is None:
                continue
            ret.append(i.strength)
        return ret

    def attack_bonus(self, g: Gear = Gear()) -> float:
        """
        Check if the character is wielding their preferred weapon.

        Character's receive a bonus if they are qielding there preferred
        weapon category. This function checks what weapon they have and
        determines that bonus.

        Parameters
        ----------
        g:  :class:`Gear`
            The `Gear` object to iterate through.

        Returns
        -------
        float:
            Either 1.1 if the preferred weapon is equipped or 1.0 if not.        
        """
        if "sword" in g.weapon.name:  # make this more dynamic of a check?
            return 1.1
        else:
            return 1.0

    def __str__(self):
        return self.name

    def __eq__(self, other):
        """
        Compare two :class:`bt_Class` objects for equality.

        Checks the name and :Class:`Stats` objects for equality.

        Parameters
        ----------
        other:  :class:`Level`
            Level object to compare this one against.

        Returns
        -------
        True if all stats are equal and the name attribute is the same.
        """
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
        self.name = "villager"
        base_stats = self.def_stats
        super(Villager, self).__init__(self.name, base_stats)

    @property
    def main_stat(self):
        return self.stats.luck

    def get_gear_stats(self, g: Gear = Gear()):
        ret = []
        for i in g:
            ret.append(i.luck)
        return ret

    @property
    def def_stats(self):
        return Stats(strength=1, agility=1, intellect=1,
                     charisma=1, con=1, luck=3)

    def attack_bonus(self, g: Gear = Gear()) -> float:
        if "pan" in g.weapon.name:
            return 1.1
        else:
            return 1.0


class Inventory:
    """
    Inventory container to hold all your precious loot.

    Contains info on the items a character holds but has not equipped.
    Additionally contains the characters wealth (coins).

    Attributes
    ----------
    contents:   :type:`list`
        The contents of the inventory.
    is_empty:   :type:`bool`
        Returns true if the inventory is empty, otherwise false.
    gold:        :type:`int`
        The amount of coins the character currently holds

    Methods
    -------
    add_item(value):
        Adds value to the inventory.
    del_item(value):
        Deletes value from the inventory.
    change_gold(value):
        Adjust gold by the amount in value. Can be positive, negative or 0.
    """
    items = []
    coins = 0
    index = -1

    def __init__(self, items: list = [], coins: int = 0):
        """
        Construct a new inventory object. By default the inventory is
        empty and contains 0 coins.
        """
        self.items = []
        self.index = -1
        self.coins = coins

    @property
    def contents(self) -> list:
        """Return a string of the names of items in the inventory"""
        out = []
        for i in self.items:
            if not isinstance(i, item.Item):
                raise TypeError("how did you get that in there?")
            out.append(i)
        return out

    def add_item(self, value: item.Equipment = None) -> list:
        """
        Add an item to the inventory container.

        Add an item to the inventory and then return the current contents
        of the inventory.

        Parameters
        ----------
        value:  :class:`item.Item`
            An item.Equipment object to insert

        Returns
        -------
        :type:`list`:
            A list containing the current items in the inventory.
        """
        if not isinstance(value, item.Item):
            raise TypeError("You can't put that in your backpack")
        self.items.append(value)
        return self.items

    def del_item(self, value: item.Item = None) -> list:
        """
        Remove an item from the inventory container.

        Remove an item from the inventory and then return the current contents
        of the inventory.

        Parameters
        ----------
        value:  :class:`item.Item`
            An item.Equipment object to remove

        Returns
        -------
        :type:`list`:
            A list containing the current items in the inventory.
        """
        if not isinstance(value, item.Item):
            raise TypeError("You can't remove that from your backpack")
        try:
            self.items.remove(value)
        except ValueError as e:
            return e
        return self.items

    @property
    def is_empty(self) -> bool:
        if len(self.items) == 0:
            return True
        else:
            return False

    @property
    def gold(self) -> int:
        return self.coins

    @gold.setter
    def gold(self, value: int = 0):
        if not isinstance(value, int):
            raise TypeError("int not passed to gold")
        if value >= 0:
            self.coins = value
        else:
            raise ValueError("why do you want to be in debt?")

    def change_gold(self, value: int = 0) -> int:
        """"
        Update the amount of coins in the inventory.

        Parameters
        ----------
        value:  :type:`int`
            The amount to change the coins value by. Any int is acceptable.
        """
        if not isinstance(value, int):
            raise TypeError("int not passed to change_gold")
        if self.coins + value < 0:
            raise ValueError("why do you want to be in debt?")
        else:
            self.coins += value
            return self.coins

    def set_gold(self, value: int = 0):
        """
        Set the amount of coins in the inventory.

        Parameters
        ----------
        value:  :type:`int`
            The amount to set the inventory contents to.
        """
        if not isinstance(value, int):
            raise TypeError("int not passed to change_gold")
        self.coins = value
        return self.coins

    def __str__(self) -> str:
        """
        Return a string with the inventory's contents.

        Coin count is NOT included in this information.
        """
        out_str = ""
        for i in self.items:
            out_str += f"{i.name}, "
        return out_str[0:len(out_str)-2]

    def __iter__(self):
        self.index = -1
        return self

    def __next__(self):
        self.index += 1
        if self.index >= len(self.items):
            raise StopIteration
        return self.items[self.index]

    def __eq__(self, other) -> bool:
        """
        Compare two :class:`Inventory` objects for equality.

        Creates a :class:`collections.Counter` object for `self.items`
        and `other.items` then compares the created dictionaries for
        equality.

        Parameters
        ----------
        other:  :class:`Inventory`
            Inventory object to compare this one against.

        Returns
        -------
        True if all stats are equal and the name attribute is the same.
        """
        if not isinstance(other, Inventory):
            return TypeError("that's not an inventory")
        temp = self.items.copy()
        other_t = other.items.copy()
        return Counter(temp) == Counter(other_t)

    def __len__(self):
        return len(self.items)


class Character:
    """The hero of the story! Contains all the important information.

    The Character class is designed to gather up all the other important
    information into one easy to reference location. The inention is to be
    able to snag all the information out of the DB create a `character.Gear`
    and a `character.Stat` then hand it all off to this object's constructor.

    Attributes
    ----------
    name:            :type:`str`
        Who are you?
    level:           :type:`int`
        Character's current level (:var:`Level.cur_level`)
    experience:      :type:`int`
        The character's experience count (:var:`Level.cur_exp`)
    stats:          :class:`character.Stats`
        This character's stat array (:var:`bt_Class.stats`)
    gear:           :class:`character.Gear`
        This character's equipped items.
    hp:             :type:`int`
        Character's current health amount. (:var:`Health.cur_hp`)
    bt_class:       :class:`character.bt_Class` 
        The class for this character. Contains class name and stats.
    strength:       :type:`int`        
        Character's strength
    agility:        :type:`int`
        Character's agility
    intellect:      :type:`int`
        Character's intellect
    charisma:       :type:`int`
        Character's charisma
    constitution:   :type:`int` 
        Character's constitution
    luck:           :type:`int`
        Character's luck
    """
    def __init__(self, name: str,
                 level: Level = Level(0, 0),
                 gear_block: Gear = Gear(),
                 class_choice: bt_Class = bt_Class('warrior'),
                 health: Health = None
                 ):
        """
        Construct a new character object

        All statistics for a character can be supplied in the constructor.

        self.health is derived from the :class:`character.bt_class` but can
        also be provided in the constructor if the default values are not
        sufficient.

        Parameters
        ----------
        name:           :type:`str`   
            The name of the new character
        level:          :class:`Level`
            A :class:`Level` to instantiate this character with. By default
            will create a :class:`Level` with 0 experience.
        class_choice    :class:`bt_Class`
            The selected class for the character. Provides the stats
            for the character.
        gear:           :class:`Gear`
            The equipped items the chaaracter has on. By default contains no
            equipment.
        health:         :class:`Health`
            The character's health, including the max and current values.
        """
        self._level = level
        self._name = name
        self._gear = gear_block
        self._bt_class = class_choice
        self._inventory = Inventory([], 10)
        if health is not None:
            self.health = health
        else:
            self.health = Health(self._bt_class.stats.constitution*10)
        return

    #  HP
    @property
    def hp(self) -> int:
        return self.health.cur_hp

    @hp.setter
    def hp(self, value) -> int:
        if not isinstance(value, int):
            raise TypeError("provide an int")
        if value > self.health.max_hp:
            raise ValueError("you cant have more than your max hp")
        self.health.cur_hp = value
        return self.health.cur_hp

    #  Level
    @property
    def level(self) -> int:
        return self._level.cur_level

    @level.setter
    def level(self, value):
        if isinstance(value, int) and value > 0:
            self._level.cur_level = value
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
            raise TypeError("Stats must be a Stats object")

    @property
    def strength(self):
        return self._bt_class.stats.strength

    @property
    def agility(self):
        return self._bt_class.stats.agility

    @property
    def intellect(self):
        return self._bt_class.stats.intellect

    @property
    def charisma(self):
        return self._bt_class.stats.charisma

    @property
    def constitution(self):
        return self._bt_class.stats.constitution

    @property
    def luck(self):
        return self._bt_class.stats.luck

    @property
    def experience(self):
        return self._level.exp

    @experience.setter
    def experience(self, value: int = 0):
        if not isinstance(value, int):
            raise TypeError("provide an int")
        if value < 0:
            raise ValueError("exp must be gt 0")
        self._level.exp = value
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
            raise TypeError("Gear must be a Gear object")
    #  End Gear

    #  Inventory
    @property
    def inventory(self) -> Inventory:
        return self._inventory

    @inventory.setter
    def inventory(self, value: Inventory):
        if isinstance(value, Inventory):
            self._inventory = value
        else:
            raise TypeError("Inventory must be an Inventory object")

    #  End Inventory

    #  ATK & DEF
    @property
    def attack(self) -> int:
        """
        The character's attack value.

        Derived from the character's main stat (:attr:`bt_Class.main_stat`),
            and the character's gear stats (:func:`bt_Class.get_gear_stats()`).

        Additionally checks :func:`bt_class.attack_bonus()` to see if the
        character is wielding their preferred weapon type.

        Returns
        -------
        A :type:`int` of the attack value.
        """
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
        """The character's defense value.

        Derived from the character's main stat (:attr:`bt_Class.main_stat`),
            and the character's gear stats (:func:`bt_Class.get_gear_stats()`).

        Additionally checks :func:`bt_Class.attack_bonus()` to see if the
        character wielding their preferred weapon type.

        Returns
        -------
        A :type:`int` of the defense value.
        """
        base = 8
        main_stat = self._bt_class.main_stat
        gear_stats = self._bt_class.get_gear_stats(self.gear)
        defense = 0
        for g in gear_stats:
            defense += g
        return int(base + (main_stat + defense) * .15)
    #  End Attack and Defense

    def gain_exp(self, value: int = 0):
        """Add exp to the character.

        Gain experience, check if you leveled up and set new level if needed.

        Parameters
        ----------
        value:   :type:`int`
            The amount of experience to add.
        """
        self._level.exp += value
        if self._level.check_next():
            self._level.cur_level += 1
            # TODO increase stats?
            # TODO give stat points for player to allocate?

    #  character.Character internal/inherited funcs #
    def __str__(self) -> str:
        """
        Return a string of character data.
        """
        # \u2764\ufe0f is red heart emoji
        # \u2618\ufe0f is the colorized shamrock emoji
        stat_str = f"Strength 💪: {self._bt_class.stats.strength}\n"\
                   f"Agility 👟: {self._bt_class.stats.agility}\n"\
                   f"Intellect 🧠: {self._bt_class.stats.intellect}\n"\
                   f"Charisma ⚡: {self._bt_class.stats.intellect}\n"\
                   f"Constitution 🐻: {self._bt_class.stats.charisma}\n"\
                   f"Luck ☘️: {self._bt_class.stats.luck}\n"

        return f"Character: {self._name}\n" \
               f"Level: {self._level}\n" \
               f"Exp: {self._level.exp} / {self._level.get_next()}\n" \
               f"Class: {self._bt_class}\n" \
               f"Gold 💰: {self._inventory.coins}\n" \
               f"Health ❤️: {self.hp}\n\n" \
               f"Stats\n------\n{stat_str}\n"

    def __eq__(self, other) -> bool:
        """
        Compare two :class:`Character` objects for equality.

        Compares the name, level (attribute NOT :class:`Level`), :class:`Gear`
        :class:`bt_class`, and :class:`Inventory` for self and other.

        If all elements are equal then True is returned. Otherwise False is 
        returned. If other is not a :class:`Character` False is also returned.

        Parameters
        ----------
        other:  :class:`Character`
            The :class:`Character` to compare the current object with.
        """
        if isinstance(other, Character):
            return self.name == other.name and self.level == other.level \
                and self.gear == other.gear \
                and self._bt_class == other._bt_class \
                and self.inventory == other.inventory
        return False
