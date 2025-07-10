import random
import time
from enum import Enum

all_items_dict = {
    "helmet": {
        "Leather cap": {"name": "Leather Cap", "attack": 1, "defence": 1, "max_HP": 5, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 10, "rarity": "common"},
        "Iron Helmet": {"name": "Iron Helmet", "attack": 0, "defence": 2, "max_HP": 10, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 30, "rarity": "common"},
        "Steel Greathelm": {"name": "Steel Greathelm", "attack": 0, "defence": 3, "max_HP": 15, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 80, "rarity": "rare"},
        "Enchanted Hood": {"name": "Enchanted Hood", "attack": 0, "defence": 1, "max_HP": 5, "intellect": 2, "max_mana": 10, "mana_regen": 1, "gold": 120, "rarity": "rare"},
        "Dragonbone Helm": {"name": "Dragonbone Helm", "attack": 2, "defence": 5, "max_HP": 25, "intellect": 2, "max_mana": 10, "mana_regen": 2, "gold": 400, "rarity": "legendary"}
    },
    "chestplate": {
        "Leather Tunic": {"name": "Leather Tunic", "attack": 0, "defence": 1, "max_HP": 10, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 15, "rarity": "common"},
        "Chainmail Shirt": {"name": "Chainmail Shirt", "attack": 0, "defence": 2, "max_HP": 15, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 40, "rarity": "common"},
        "Iron Breastplate": {"name": "Iron Breastplate", "attack": 0, "defence": 4, "max_HP": 20, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 100, "rarity": "rare"},
        "Elven Cuirass": {"name": "Elven Cuirass", "attack": 1, "defence": 3, "max_HP": 15, "intellect": 2, "max_mana": 10, "mana_regen": 1, "gold": 180, "rarity": "rare"},
        "Dragon Scale Armor": {"name": "Dragon Scale Armor", "attack": 2, "defence": 6, "max_HP": 30, "intellect": 3, "max_mana": 15, "mana_regen": 2, "gold": 800, "rarity": "legendary"}
    },
    "leg armor": {
        "Cloth Trousers": {"name": "Cloth Trousers", "attack": 0, "defence": 1, "max_HP": 5, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 8, "rarity": "common"},
        "Leather Greaves": {"name": "Leather Greaves", "attack": 0, "defence": 2, "max_HP": 8, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 20, "rarity": "common"},
        "Iron Leggings": {"name": "Iron Leggings", "attack": 0, "defence": 3, "max_HP": 12, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 60, "rarity": "rare"},
        "Knight's Platelegs": {"name": "Knight's Platelegs", "attack": 0, "defence": 4, "max_HP": 18, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 120, "rarity": "rare"},
        "Shadowstep Pants": {"name": "Shadowstep Pants", "attack": 1, "defence": 3, "max_HP": 15, "intellect": 2, "max_mana": 10, "mana_regen": 2, "gold": 350, "rarity": "legendary"}
    },
    "shoes": {
        "Worn Boots": {"name": "Worn Boots", "attack": 0, "defence": 1, "max_HP": 2, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 5, "rarity": "common"},
        "Leather Boots": {"name": "Leather Boots", "attack": 0, "defence": 1, "max_HP": 4, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 12, "rarity": "common"},
        "Iron Sabatons": {"name": "Iron Sabatons", "attack": 0, "defence": 2, "max_HP": 8, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 35, "rarity": "rare"},
        "Swiftfoot Sandals": {"name": "Swiftfoot Sandals", "attack": 1, "defence": 1, "max_HP": 6, "intellect": 1, "max_mana": 5, "mana_regen": 1, "gold": 90, "rarity": "rare"},
        "Boots of Levitation": {"name": "Boots of Levitation", "attack": 0, "defence": 2, "max_HP": 10, "intellect": 3, "max_mana": 10, "mana_regen": 2, "gold": 300, "rarity": "legendary"}
    },
    "weapon": {
        "Rusty Sword": {"name": "Rusty Sword", "attack": 2, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 15, "rarity": "common"},
        "Iron Axe": {"name": "Iron Axe", "attack": 3, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 25, "rarity": "common"},
        "Elven Bow": {"name": "Elven Bow", "attack": 4, "defence": 0, "max_HP": 0, "intellect": 1, "max_mana": 0, "mana_regen": 0, "gold": 70, "rarity": "rare"},
        "Wizard's Staff": {"name": "Wizard's Staff", "attack": 2, "defence": 0, "max_HP": 0, "intellect": 4, "max_mana": 10, "mana_regen": 2, "gold": 120, "rarity": "rare"},
        "Dragonfang Dagger": {"name": "Dragonfang Dagger", "attack": 7, "defence": 1, "max_HP": 0, "intellect": 2, "max_mana": 0, "mana_regen": 0, "gold": 500, "rarity": "legendary"}
    },
    "shield": {
        "Wooden Shield": {"name": "Wooden Shield", "attack": 0, "defence": 2, "max_HP": 5, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 10, "rarity": "common"},
        "Iron Buckler": {"name": "Iron Buckler", "attack": 0, "defence": 3, "max_HP": 8, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 25, "rarity": "common"},
        "Tower Shield": {"name": "Tower Shield", "attack": 0, "defence": 5, "max_HP": 15, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 90, "rarity": "rare"},
        "Aegis of Light": {"name": "Aegis of Light", "attack": 1, "defence": 6, "max_HP": 20, "intellect": 2, "max_mana": 5, "mana_regen": 1, "gold": 200, "rarity": "rare"},
        "Mirror Shield": {"name": "Mirror Shield", "attack": 2, "defence": 8, "max_HP": 25, "intellect": 3, "max_mana": 10, "mana_regen": 2, "gold": 700, "rarity": "legendary"}
    },
    "ring": {
        "Copper Ring": {"name": "Copper Ring", "attack": 0, "defence": 0, "max_HP": 2, "intellect": 1, "max_mana": 2, "mana_regen": 0, "gold": 5, "rarity": "common"},
        "Silver Band": {"name": "Silver Band", "attack": 0, "defence": 1, "max_HP": 3, "intellect": 1, "max_mana": 3, "mana_regen": 0, "gold": 12, "rarity": "common"},
        "Ring of Protection": {"name": "Ring of Protection", "attack": 0, "defence": 2, "max_HP": 5, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 40, "rarity": "rare"},
        "Ring of Fire": {"name": "Ring of Fire", "attack": 2, "defence": 0, "max_HP": 0, "intellect": 2, "max_mana": 5, "mana_regen": 1, "gold": 100, "rarity": "rare"},
        "Ring of Invisibility": {"name": "Ring of Invisibility", "attack": 1, "defence": 2, "max_HP": 5, "intellect": 3, "max_mana": 10, "mana_regen": 2, "gold": 400, "rarity": "legendary"}
    },
    "necklace": {
        "Simple Pendant": {"name": "Simple Pendant", "attack": 0, "defence": 0, "max_HP": 2, "intellect": 1, "max_mana": 2, "mana_regen": 0, "gold": 8, "rarity": "common"},
        "Amulet of Health": {"name": "Amulet of Health", "attack": 0, "defence": 1, "max_HP": 8, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 20, "rarity": "common"},
        "Necklace of Wisdom": {"name": "Necklace of Wisdom", "attack": 0, "defence": 0, "max_HP": 3, "intellect": 3, "max_mana": 5, "mana_regen": 1, "gold": 60, "rarity": "rare"},
        "Choker of Shadows": {"name": "Choker of Shadows", "attack": 1, "defence": 1, "max_HP": 5, "intellect": 2, "max_mana": 8, "mana_regen": 2, "gold": 150, "rarity": "rare"},
        "Dragon Tooth Amulet": {"name": "Dragon Tooth Amulet", "attack": 2, "defence": 2, "max_HP": 10, "intellect": 4, "max_mana": 15, "mana_regen": 3, "gold": 600, "rarity": "legendary"}
    },
    "artifact": {
        "Ancient Relic": {"name": "Ancient Relic", "attack": 1, "defence": 1, "max_HP": 5, "intellect": 1, "max_mana": 2, "mana_regen": 0, "gold": 50, "rarity": "common"},
        "Orb of Power": {"name": "Orb of Power", "attack": 3, "defence": 2, "max_HP": 10, "intellect": 3, "max_mana": 10, "mana_regen": 1, "gold": 200, "rarity": "common"},
        "Phoenix Feather": {"name": "Phoenix Feather", "attack": 2, "defence": 2, "max_HP": 8, "intellect": 4, "max_mana": 12, "mana_regen": 2, "gold": 300, "rarity": "rare"},
        "Cursed Idol": {"name": "Cursed Idol", "attack": 4, "defence": 0, "max_HP": 0, "intellect": 5, "max_mana": 15, "mana_regen": 3, "gold": 400, "rarity": "rare"},
        "Tome of Forgotten Lore": {"name": "Tome of Forgotten Lore", "attack": 5, "defence": 3, "max_HP": 15, "intellect": 7, "max_mana": 20, "mana_regen": 4, "gold": 2000, "rarity": "legendary"}
    },
    "potions": {
        "Health Potion": {"name": "Health Potion", "attack": 0, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 15, "rarity": "common"},
        "Mana Potion": {"name": "Mana Potion", "attack": 0, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 18, "rarity": "common"},
        "Potion of Strength": {"name": "Potion of Strength", "attack": 0, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 40, "rarity": "rare"},
        "Potion of Wisdom": {"name": "Potion of Speed", "attack": 0, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 45, "rarity": "rare"},
        "Elixir of Immortality": {"name": "Elixir of Immortality", "attack": 0, "defence": 0, "max_HP": 0, "intellect": 0, "max_mana": 0, "mana_regen": 0, "gold": 500, "rarity": "legendary"}
    }
}

# hero equipped items will look like this:

# hero_items_equipped = {
#     "helmet" : item_object, "chestplate" : item_object2
# }


# hero inventory items will look like this:

# hero_items = {
#    "helmet": {"(item_name)": item_object, "(item_name2)": item_object2 ... etc}
#        ...
# }

hero_items_empty = {
    "helmet": {},
    "chestplate": {},
    "leg armor": {},
    "shoes": {},
    "weapon": {},
    "shield": {},
    "ring": {},
    "necklace": {},
    "artifact": {},
    "potions": {}
}

# Chances of items of different rarities to spawn depending on the biome
items_spawn_biomes = {
    "Forest":{
        "common": 0.8, "rare": 0.2 # here "common" item has 80% and "rare" item has 20% chance to spawn
    },
    "Swamp":{
        "common": 0.6, "rare": 0.4
    },
    "Cursed land":{
        "common": 0.4, "rare": 0.4, "legendary": 0.2 
    },
    "Magma hills":{
        "common": 0.2, "rare": 0.4, "legendary": 0.4 
    },
    "EMPTY_BIOME":{
        "common": 0.2, "rare": 0.4, "legendary": 0.4 
    }
}

# define potions effects
class potion_buffs(Enum):

    health_potion_HP_regen = 50
    mana_potion_mana_regen = 50
    potion_of_strength_attack_bonus = 5
    potion_of_wisdom_intellect_bonus = 5
    potion_of_immortality_max_HP_bonus = 100

class item_class:
    def __init__(self, 
                 name,
                 item_type,
                 attack, 
                 defence, 
                 max_HP, 
                 intellect, 
                 max_mana,
                 mana_regen,
                 gold,
                 rarity):
        self.name = name
        self.item_type = item_type
        self.attack_bonus = attack
        self.defence_bonus = defence
        self.max_HP_bonus = max_HP
        self.intellect_bonus = intellect
        self.max_mana_bonus = max_mana
        self.mana_regen_bonus = mana_regen
        self.gold = gold
        self.rarity = rarity

    @classmethod
    def item_from_name(cls, item_name_looking: str):

        for item_type in all_items_dict.keys():
            for item_name, item_data in all_items_dict[item_type].items():
                if item_data["name"] == item_name_looking:
                    return cls(**item_data, item_type = item_type)
        print("No such item found")
        time.sleep(1)

    def spawn_item(self, biome: str):

        # Getting random item type
        random_item_type = random.choice(tuple((all_items_dict.keys())))
        item_type_dict = all_items_dict.get(random_item_type)


        # Getting random item from selected type
        item_spawn_chances_dict = items_spawn_biomes.get(biome)

        # Choosing the rarity of the item
        spawn_chance = tuple(item_spawn_chances_dict.values())
        rarity = tuple(item_spawn_chances_dict.keys())
        item_rarity = random.choices(rarity, spawn_chance, k=1)[0]
        print(f"Item type is:{item_type_dict.keys()}")
        print(f"Item rarity is: {item_rarity} in biome {biome}")
        # check if such item is present in dictionary
        rarity_present = False
        for key in item_type_dict.keys():
            item_rarity_check = item_type_dict.get(key)
            if item_rarity_check.get("rarity") == item_rarity:
                rarity_present = True
        
        if rarity_present == False:
            print(f"Item of such rarity ({print(rarity)}) not found")
            print("CHECK DICTIONARY")
            exit(0)

        # iterating and finding the item of the correct rarity for biome
        random_item_name = random.choice(tuple(item_type_dict.keys()))
        item_dict = item_type_dict.get(random_item_name)

        while item_dict.get("rarity") != item_rarity:
            
            random_item_name = random.choice(tuple(item_type_dict.keys()))
            item_dict = item_type_dict.get(random_item_name)

        # Assigning its bonuses to item object
        self.name = item_dict.get("name")
        self.item_type = random_item_type
        self.attack_bonus = item_dict.get("attack")
        self.defence_bonus = item_dict.get("defence")
        self.max_HP_bonus = item_dict.get("max_HP")
        self.intellect_bonus = item_dict.get("intellect")
        self.max_mana_bonus = item_dict.get("max_mana")
        self.mana_regen_bonus = item_dict.get("mana_regen")
        self.gold = item_dict.get("gold")
        self.rarity = item_dict.get("rarity")

    def display_item_stats(self):
        
        for item_type in all_items_dict.keys():
            for item_name in all_items_dict[item_type].keys():
                for key, value in all_items_dict[item_type][item_name].items():
                    if all_items_dict[item_type][item_name]["name"] == self.name:
                        if not isinstance(value, str) and value != 0:
                            if key == "max_HP": key = "max HP"
                            elif key == "max_mana": key = "max mana"
                            elif key == "mana_regen": key = "mana regen"
                            print(f"{key} {value}", end=" | ")