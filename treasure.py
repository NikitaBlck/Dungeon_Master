import random
from items import item_class

chestGold_amount_biomes = {
    "Forest":{
        "min": 100, "max": 200 # here chest from "Forest" biome can contain from 100 to 200 gold
    },
    "Swamp":{
        "min": 100, "max": 200
    },
    "Cursed land":{
        "min": 100, "max": 200 
    },
    "Magma hills":{
        "min": 100, "max": 200
    },
    "EMPTY_BIOME":{
        "min": 100, "max": 200
    }
}

class treasure_class:
    def __init__(self):
        # initialize both gold and item object attributes so that one of them is not Null
        self.gold = 0
        self.item = None

    def spawn_treasure(self, biome:str):
        # set item spawn chance
        if random.random() < 0.7:
            # spawn item in the treasure
            self.item = item_class(name=None, item_type=None, attack=0, defence=0, max_HP=0, intellect=0, max_mana=0, mana_regen=0, gold=0, rarity=None)
            self.item.spawn_item(biome)
            print(f"Treasure has {self.item.name} item ({self.item.rarity})")
        else:
            # spawn gold in the treasure
            gold_range = chestGold_amount_biomes.get(biome)
            self.gold = random.choice(range(gold_range.get("min"), gold_range.get("max") + 1, 10))
            print(f"Treasure has {self.gold} gold")
