class Item:
    def __init__(self, name: str, value: int = 0):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if not isinstance(other, Item):
            return False
        else:
            return self.name == other.name
        
    def __lt__(self, other):
        if not isinstance(other, Item):
            return False
        else:
            return self.name < other.name


class Slot:
    """A super class representing the possible gear slots for a character.

    A wrapper class for some basic data on slots for character equipment.
    Generally meant to be used as a super class for a specific equipment
    slot.
    slot_id is a unique ID for each possible slot on a character,
    intended to be scalable and modifiable as needed in the future.

    Attributes:
        slot    The text representation of the slot. ex slot 0 is 'head'"""

    #  im sure theres a better way to maintain this
    slots = {
        0: 'head',
        1: 'chest',
        2: 'arms',
        3: 'legs',
        4: 'hands',
        5: 'finger',
        6: 'trinket',
        7: 'weapon',
        8: 'offhand',
    }
    rev_slots = {
        'head': 0,
        'chest': 1,
        'arms': 2,
        'legs': 3,
        'hands': 4,
        'finger': 5,
        'trinket': 6,
        'weapon': 7,
        'offhand': 8,
    }

    def __init__(self, slot_id=0):
        """Create a Slot.

        Parameters
        ----------
        slot_id An integer that represents a slot in Slot.slots

        Raises
        ----------
        ValueError Raises a ValueError if an int x<0 or x>len(slots), or
            when a str is passed but the str is not in the allowed list.
        TypeError   Raises a type error if a type other than int or str is
            passed.
        """
        if isinstance(slot_id, str):
            if slot_id in self.rev_slots.keys():
                self.slot_id = self.rev_slots[slot_id]
                return
            else:
                raise ValueError("please provide a valid str")
        if not isinstance(slot_id, int):
            raise TypeError("please provide an int or valid str")
        if slot_id < 0 or slot_id > len(self.slots):
            raise ValueError("Please provide an allowed value "
                             f"[0 <= {slot_id} <={len(self.slots)}]")
        else:
            self.slot_id = slot_id
            return

    @property
    def slot(self, what: int):
        return self.slots[what]

    @slot.setter
    def slot(self, slot_id):
        self.slot_id = slot_id

    def __str__(self) -> str:
        return self.slots[self.slot_id]


class Material:
    """Material type used by items (weapons and armor).

    This class is intended to be used by the `item.Item` class to store
    details on the item's material and tier. Allowing for adding
    new properties in the future.

    Attributes:
        material_type   The type of the material. A string representing
            the material name.
        material_tier   A tier representing how powerful the material
            is compared to others
        name            The same as material type (references the same
                            internal variable)
        valid_slots       A list of valid slot_ids for this material"""

    def __init__(self, material_type: str = None,
                 material_tier: float = 0,
                 *args, **kwargs):
        """Construct a new Material from the provided material type and tier

        Creates a new object based on the tier and type provided. Currently
        type is a string of some relevant material like 'iron'. Tier is
        intended to represent the relative power of two different materials.

        Parameters
        ----------
        material_type   A string representation of the materials type.
        material_tier   An integer representing the relative power of the
            material.
        *args           If "all" is provided all slots available in Slot.slots
            are added. If a Slot is passed then the Slot.slot_id is added,
            finally if any integers are passed it is appended directly.
        **kwargs        If "slots" is passed as a kwarg the valid list is
            copied into the _valid variable. Any arguments passed in *args
            are ignored in this case.
        """
        self._material_type = material_type
        self._material_tier = material_tier
        self.valid = []
        try:
            kwargs['slots']
        except KeyError:
            kwargs['slots'] = None
        if kwargs['slots'] is not None\
                and isinstance(kwargs['slots'], list):
            self.valid = kwargs['slots'].copy()
        else:
            for arg in args:
                if isinstance(arg, str) and "all" in str:
                    for i in range(0, len(Slot.slots)):
                        self.valid.append(i)
                if isinstance(arg, Slot):
                    self.valid.append(Slot.slot_id)
                if isinstance(arg, list):
                    for e in arg:
                        if isinstance(e, Slot):
                            self.valid.append(e)
                if isinstance(arg, int) and arg in Slot.slots.values():
                    self.valid.append(arg)
            temp = []
            [temp.append(x) for x in self.valid if x not in temp]
            self.valid = temp.copy()

    @property
    def material_type(self) -> str:
        return self._material_type

    @material_type.setter
    def material_type(self, value: str):
        if isinstance(value, str):
            self._material_type = value
        else:
            raise ValueError("Material type must be a string.")

    @property
    def name(self) -> str:
        return self._material_type

    @name.setter
    def name(self, value: str):
        if isinstance(value, str):
            self._material_type = value
        else:
            raise ValueError("Material type must be a string.")

    @property
    def material_tier(self) -> int:
        return self._material_tier

    @material_tier.setter
    def material_tier(self, value: int):
        if isinstance(value, int) and value >= 0:
            self._material_tier = value
        else:
            raise ValueError("Material tier must be a non-negative integer.")

    @property
    def valid_slots(self) -> list:
        r = []
        for s in self.valid:
            r.append(s.slot_id)
        return r

    def __str__(self) -> str:
        out = f"Material Type: {self._material_type}, " \
               f"Material Tier: {self._material_tier}, " \
               f"Valid for: "
        for m in self.valid:
            out += str(m)+", "
        return out[0:len(out)-2]


#  TODO create an Item superclass
class Equipment(Item):
    """Equipment super class

    The super class for all equipment type items. Containing the properties
        shared for all equipment. Generally should inherited by a specific
        equipment type (based on an `item.Slot`)

    Attributes:
        name    A string representing the name of the equipment.
                    Typically formed by combining the material and slot
        item_id A unique ID assigned to this equipment.
        slot    An `item.Slot` for this equipment
        material An `item.Materia`l for this equipment
        strength The strength bonus this equipment grants
        agility The agility bonus this equipment grants
        intellect The intellect bonus this equipment grants
        charisma The charisma bonus this equipment grants
        constitution The constitution bonus this equipment grants
        luck The luck bonus this equipment grants"""
    def __init__(self, *args, **kwargs):
        self._name = kwargs['name']
        self._item_id = kwargs['item_id']
        self._slot = kwargs['slot']
        self._b_strength = kwargs['strength']
        self._b_agility = kwargs['agility']
        self._b_intellect = kwargs['intellect']
        self._b_charisma = kwargs['charisma']
        self._b_constitution = kwargs['constitution']
        self._b_luck = kwargs['luck']
        self._material = kwargs['material']
        if self._slot.slot_id not in self.material.valid_slots:
            raise ValueError("this type is not valid for this slot "
                             f"slot_id: {self.slot.slot_id}"
                             f"valid_ids: {self.material.valid}")

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def item_id(self) -> int:
        return self._item_id

    @item_id.setter
    def item_id(self, value: int):
        self._item_id = value

    @property
    def slot(self) -> str:
        return self._slot

    @slot.setter
    def slot(self, value: str):
        self._slot = value

    @property
    def strength(self) -> int:
        return self._b_strength

    @strength.setter
    def strength(self, value: int):
        self._b_strength = value

    @property
    def agility(self) -> int:
        return self._b_agility

    @agility.setter
    def agility(self, value: int):
        self._b_agility = value

    @property
    def intellect(self) -> int:
        return self._b_intellect

    @intellect.setter
    def intellect(self, value: int):
        self._b_intellect = value

    @property
    def charisma(self) -> int:
        return self._b_charisma

    @charisma.setter
    def charisma(self, value: int):
        self._b_charisma = value

    @property
    def constitution(self) -> int:
        return self._b_constitution

    @constitution.setter
    def constitution(self, value: int):
        self._b_constitution = value

    @property
    def luck(self) -> int:
        return self._b_luck

    @luck.setter
    def luck(self, value: int):
        self._b_luck = value

    @property
    def material(self) -> Material:
        return self._material

    @material.setter
    def material(self, new_material: Material = Material("wood", 0)):
        self._material = new_material

    def __str__(self) -> str:
        return (f"Item: {self._name} (ID: {self._item_id}), "
                f"Slot: {self._slot},"
                f"Material: {self.material.material_type}, "
                f"({self.material.material_tier}), "
                f"Strength: {self._b_strength}, "
                f"Agility: {self._b_agility}, "
                f"Intellect: {self._b_intellect}, "
                f"Charisma: {self._b_charisma}, "
                f"Constitution: {self._b_constitution}, "
                f"Luck: {self._b_luck}")


class Head(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(0)
        super(Weapon, self).__init__(**kwargs)


class Chest(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(1)
        super(Weapon, self).__init__(**kwargs)


class Arms(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(2)
        super(Weapon, self).__init__(**kwargs)


class Legs(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(3)
        super(Weapon, self).__init__(**kwargs)


class Hands(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(4)
        super(Weapon, self).__init__(**kwargs)


class Ring(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(5)
        super(Weapon, self).__init__(**kwargs)


class Trinket(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(6)
        super(Weapon, self).__init__(**kwargs)


class Weapon(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(7)
        super(Weapon, self).__init__(**kwargs)


class OffHand(Equipment):
    def __init__(self, **kwargs):
        self._slot = Slot(8)
        super(Weapon, self).__init__(**kwargs)
