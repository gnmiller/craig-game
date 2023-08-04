import item

base_mats_prefix = ["wood", "stone", "bone"]
metals_prefix = ["copper", "bronze", "iron", "steel", "mithril", "adamantine"]
prec_metals_prefix = ["copper", "gold", "silver", "mithril", "adamantine"]

weapon_suffix = ["sword", "bow", "staff", "frying_pan", "mace", "axe"]
armor_suffix = ["armor", "legguards", "gloves", "boots"]
ring_suffx = ["ring", "band", "loop", "hoop"]

m = [("wood", 0, "all"),
     ("stone", 1, "all"),
     ("bone", 2, "all"),
     ("copper", 3, "all"),
     ("silver", 4, "all"),
     ("bronze", 4, "all"),
     ("iron", 5, "all"),
     ("steel", 6, "all"),
     ("bronze", 7, "all"),
     ("mithril", 8, "all"),
     ("adamantine", 9, "all")
     ]
slots = []
for k, v in item.Slot.slots.items():
    slots.append(item.Slot(k))
for i in slots:
    print(i)

#  basic materials
test_mat = item.Material("test", 1000, slots)
basic_materials = {
    'wood': item.Material("wood", 0, slots),
    'stone': item.Material("stone", 0.5, slots),
    'bone': item.Material("bone", 1, slots),

    'copper': item.Material("copper", 3, slots),
    'iron': item.Material("iron", 5, slots),
    'steel': item.Material("steel", 7, slots),
    'mithril': item.Material("mithril", 10, slots),

    'silver': item.Material("silver", 6, 5),
    'gold': item.Material("gold", 9, 5),
    'diamond': item.Material("diamond", 15, slots)
}

item_id = 0
#  basic items
bw = {}
for k, v in basic_materials.items():
    for slot in weapon_suffix:
        name = f"{k} {v}"
        bw[name] = item.Weapon(name=name, item_id=item_id, slot=item.Slot('weapon'), material=v,
                               strength=0, agility=0, intellect=0, charisma=0, constitution=0, luck=0)
        item_id += 1

for k, v in bw.items():
    print(k, v)
