from enum import Enum
import time
from items import item_class
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from characters import hero_class

class shopSizes(Enum):

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class shopClass:

    def __init__(self, size: Enum, biome: str, items_available: dict):
        self.size = size
        self.biome = biome
        self.items_available = items_available
        if size == shopSizes.SMALL: self.items_number = 6
        if size == shopSizes.MEDIUM: self.items_number = 8
        if size == shopSizes.LARGE: self.items_number = 10

    @classmethod
    def shop_from_json(cls, data):
        
        size = data["size"]
        biome = data["biome"]
        items_available = data["items_available"]

        return cls(size, biome, items_available)
    
    def refresh_items_available(self):

        while len(self.items_available) < self.items_number:

            item = item_class(name=None, item_type=None, attack=0, defence=0, max_HP=0, intellect=0, max_mana=0, mana_regen=0, gold=0, rarity=None)
            item.spawn_item(self.biome)

            self.items_available[item.name] = item
        print(self.items_available)

    def display_items_available(self):

        for key, value in  self.items_available.items():
            value:item_class
            print(f"{key}:", end=" ")
            value.display_item_stats()
            print()
        print()
    
    def sell_item(self, item_name: str, hero: "hero_class") -> item_class:

        # Look for item in shop items and delete item if found
        for item_selected_name, item_selected in  self.items_available.items():
            if item_selected_name == item_name:
                if hero.gold >= item_selected.gold:
                    item_to_sell = item_selected
                    del self.items_available[item_selected_name]
                    return item_to_sell
                else:
                    print("Not enough gold")
                    time.sleep(1.5)
                    return 0
        print("Item doesn't exist")
        time.sleep(1.5)
        return 0