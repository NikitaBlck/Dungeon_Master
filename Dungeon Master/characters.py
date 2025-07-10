import time
from enum import Enum
from spell import all_spells , SPELL_LOOKUP, spell_Names, spell_class
from dataclasses import dataclass
from typing import TYPE_CHECKING
from items import item_class, potion_buffs

@dataclass(frozen=True)
class heroLevelUpBonusesClass:
    attack: int
    defence: int
    max_HP: int
    HP_regen: int
    intellect: int
    max_mana: int
    mana_regen: int

heroActiveLvlUpBonuses = heroLevelUpBonusesClass(attack=1,
                                                 defence=1,
                                                 max_HP=10,
                                                 HP_regen=1,
                                                 intellect=1,
                                                 max_mana=5,
                                                 mana_regen=1
                                                 )

# Define base class for inheritance
class character:
    def __init__(self, name: str, attack_attribute: int, defence_attribute: int, max_HP: int):
        self.name = name
        self.attack_attribute = attack_attribute
        self.defence_attribute = defence_attribute
        self.max_HP = max_HP
        self.HP = max_HP

    def attack(self, target: "character"):
        
        # reduce damage by 1 for each 3 points of defence of an attack target
        damage_reduction = int(target.defence_attribute / 3)
        # calculate damage and prevent damage getting less than 0
        damage = max(self.attack_attribute - damage_reduction, 0)

        target.HP -= damage
        print(f"{self.name} did {damage} damage to {target.name}")

# Define hero class (inherited from character)
class hero_class(character):
    def __init__(
        self,
        name: str,
        attack_attribute: int,
        defence_attribute: int,
        max_HP: int,
        HP_regen: int,
        intellect: int,
        max_mana: int,
        mana_regen: int,
        items: dict,
        items_equipped: dict,
        level: int,
        gold: int,
        xp: int,
        xp_until_next_lvl: int,
        pos: list,
        icon: str
    ):
        super().__init__(name, attack_attribute, defence_attribute, max_HP)
        self.HP_regen = HP_regen
        self.intellect = intellect
        self.max_mana = max_mana
        self.mana = max_mana
        self.mana_regen = mana_regen
        self.items = items
        self.items_equipped = items_equipped
        self.level = level
        self.gold = gold
        self.xp = xp
        self.xp_until_next_lvl = xp_until_next_lvl
        self.pos = pos
        self.icon = icon

        # add all the attributes that are missing

    def drop_item(self, item_type_to_drop: str):
        
            # Check if such item is equipped
            if self.items_equipped.get(item_type_to_drop):
                
                # Copy equipped item to the inventory
                old_item_object: item_class
                old_item_object = self.items_equipped.get(item_type_to_drop)
                self.items[item_type_to_drop][old_item_object.name] = self.items_equipped.get(item_type_to_drop)

                self.attack_attribute -= getattr(old_item_object, "attack_bonus", 0)
                self.defence_attribute -= getattr(old_item_object, "defence_bonus", 0)
                self.max_HP -= getattr(old_item_object, "max_HP_bonus", 0)
                self.intellect -= getattr(old_item_object, "intellect_bonus", 0)
                self.max_mana -= getattr(old_item_object, "max_mana_bonus", 0)
                self.mana_regen -= getattr(old_item_object, "mana_regen_bonus", 0)

                # Delete equipped item
                del self.items_equipped[item_type_to_drop]
                print(f"item deleted {self.items_equipped.get(item_type_to_drop)}")
            else:
                print("such item doesn't exist")
                time.sleep(2)
                return

    def equip_item(self, item_name_to_equip: str):
        
        item = None
        # Looking for the item object in hero inventory
        for type_key in self.items.keys():
            item_type_dict = dict(self.items.get(type_key))
            if item_type_dict:
                for key in item_type_dict.keys():
                    if key == item_name_to_equip:
                        item = item_type_dict.get(key)
#                        print(f"found a {key} item! object ({item})")
#                        input()
        
        if item == None:
            print("Such item doesn't exist")
            time.sleep(2)
            return 0
        
        item: item_class

        # Move equipped item to inventory if there is already item of such type equipped
        if self.items_equipped.get(item.item_type): self.drop_item(item.item_type)
            
        # equip new item
        self.items_equipped[item.item_type] = item
        # Delete new item from inventory items
        del self.items[item.item_type][item.name]

        # give hero bonuses from items
        self.attack_attribute += getattr(item, "attack_bonus", 0)
        self.defence_attribute += getattr(item, "defence_bonus", 0)
        self.max_HP += getattr(item, "max_HP_bonus", 0)
        self.intellect += getattr(item, "intellect_bonus", 0)
        self.max_mana += getattr(item, "max_mana_bonus", 0)
        self.mana_regen += getattr(item, "mana_regen_bonus", 0)

        # debug printouts
        print("Hero has: ")
        for key, value in self.items_equipped.items():
            if self.items_equipped.get(key):
                item_object_test: item_class
                item_object_test = value
                print(f"{key}, {value}, {item_object_test.name}")


    def print_equipped(self):

        print("Hero's equipment:\n")
        for slot in [
            "helmet", "chestplate", "leg armor", "shoes", "weapon",
            "shield", "ring", "necklace", "artifact", "potions"
        ]:
            item = self.items_equipped.get(slot)
            if item:
                print(f"{slot}: {item.name}")
            else:
                print(f"{slot}: None")
        print()

# This function is for testing only!!!

    def print_inventory(self):

        print(f"{self.name}'s inventory:")
        for type_key in self.items.keys():
            items_dict = dict(self.items.get(type_key))
            if items_dict:
                print(f"{type_key} items: ", end="")
                for key in items_dict.keys():
                    print(f"{key}", end= " | ")
                print()


# This function is for testing only!!!

    def pick_up_item(self, pickedUp_item: "item_class"):
         # move picked up item to the inventory
         self.items[pickedUp_item.item_type][pickedUp_item.name] = pickedUp_item
         # Debugging printouts
         print("Hero now has:")
         for type_key in self.items.keys():
             items_dict = dict(self.items.get(type_key))
             if items_dict:
                 print(f"{type_key} type:")
                 for key in items_dict.keys():
                     print(f"{key}", end= " ")
                 print()
         print("\n\nInventory read")

    def pick_up_treasure(self, treasure_gold: int, treasure_item: "item_class"):

        print("You have found a treasure")
        # if treasure has gold, give player gold found in treasure
        if treasure_gold > 0:
            print(f"+ {treasure_gold}")
            self.gold += treasure_gold
            print(f"Hero got {self.gold} gold")

        # if treasure has item, move it to inventory
        if treasure_item:
            self.items[treasure_item.item_type][treasure_item.name] = treasure_item
            print(treasure_item.name, end=": ")
            treasure_item.display_item_stats()
            print()

    def level_up(self):
        # give player a new level and reset current xp
        self.level += 1
        self.xp -= self.xp_until_next_lvl
        # restore health and mana
        self.HP = self.max_HP
        self.mana = self.max_mana

        while True:

            print(f"You have reached level {self.level}!\n")
            # Ask player which attribute to increase
            print("Select attribute to increase\n"
                f"1. +{heroActiveLvlUpBonuses.attack} Attack\n"
                f"2. +{heroActiveLvlUpBonuses.defence} Defence\n"
                f"3. +{heroActiveLvlUpBonuses.intellect} Intellect\n"
                f"4. +{heroActiveLvlUpBonuses.max_HP} Max HP\n"
                f"5. +{heroActiveLvlUpBonuses.HP_regen} HP Regen\n"
                f"6. +{heroActiveLvlUpBonuses.max_mana} Max Mana\n"
                f"7. +{heroActiveLvlUpBonuses.mana_regen} Mana Regen\n")
            
            level_up_choice = input()
            match level_up_choice:
                case "1": self.attack_attribute += heroActiveLvlUpBonuses.attack
                case "2": self.defence_attribute += heroActiveLvlUpBonuses.defence
                case "3": self.intellect += heroActiveLvlUpBonuses.intellect
                case "4": self.max_HP += heroActiveLvlUpBonuses.max_HP
                case "5": self.HP_regen += heroActiveLvlUpBonuses.HP_regen
                case "6": self.max_mana += heroActiveLvlUpBonuses.max_mana
                case "7": self.mana_regen += heroActiveLvlUpBonuses.mana_regen
                case _: continue
            break
        
        # make the next level harder to reach
        self.xp_until_next_lvl *= 2

    def hero_death(self):
        print("You have died")
        time.sleep(2)
        self.pos = [0, 0]
        self.gold = int(self.gold * 0.5)
        self.HP = self.max_HP

    def drink_potion(self) -> str:

        match self.items_equipped["potions"].name:
            case "Health Potion":
                self.HP += potion_buffs.health_potion_HP_regen.value
                if self.HP > self.max_HP: self.HP = self.max_HP
                print(f"You drank {self.items_equipped["potions"].name} and got +{potion_buffs.health_potion_HP_regen.value} to HP")
            case "Mana Potion":
                self.mana += potion_buffs.mana_potion_mana_regen.value
                if self.mana > self.max_mana: self.mana = self.max_mana
                print(f"You drank {self.items_equipped["potions"].name} and got +{potion_buffs.mana_potion_mana_regen.value} to mana")
            case "Potion of Strength":
                self.attack_attribute += potion_buffs.potion_of_strength_attack_bonus.value
                print(f"You drank {self.items_equipped["potions"].name} and got +{potion_buffs.potion_of_strength_attack_bonus.value} to attack")
            case "Potion of Wisdom":
                self.intellect += potion_buffs.potion_of_wisdom_intellect_bonus.value
                print(f"You drank {self.items_equipped["potions"].name} and got +{potion_buffs.potion_of_wisdom_intellect_bonus.value} to intellect")
            case "Elixir of Immortality":
                self.max_HP += potion_buffs.potion_of_immortality_max_HP_bonus.value
                print(f"You drank {self.items_equipped["potions"].name} and got +{potion_buffs.potion_of_immortality_max_HP_bonus.value} to max HP")
            case _:
                print("No potion equipped")
                time.sleep(2)
                return 0
        time.sleep(1.5)
        return self.items_equipped["potions"].name
    
    def reset_potion_effects(self, drank_potion_name) -> None:
        if drank_potion_name:
            match drank_potion_name:
                case "Potion of Strength":
                    self.attack_attribute -= potion_buffs.potion_of_strength_attack_bonus.value
                case "Potion of Wisdom":
                    self.intellect -= potion_buffs.potion_of_wisdom_intellect_bonus.value
                case "Elixir of Immortality":
                    self.max_HP -= potion_buffs.potion_of_immortality_max_HP_bonus.value
                case _:
                    return
        return
    
    def restore_after_battle(self, HP_pre_battle, mana_pre_battle):
        
        # Restore HP if it is less than before battle
        self.HP = min(self.HP + self.HP_regen, HP_pre_battle)
        self.mana = min(self.mana + self.mana_regen, mana_pre_battle)
    
    def buy_item(self, item_to_buy: item_class):

        self.items[item_to_buy.item_type][item_to_buy.name] = item_to_buy
        self.gold -= item_to_buy.gold
    
    def find_item(self, looking_item_name: str) -> item_class:

        for equipped_item_type, equipped_item in self.items_equipped.items():
            if self.items_equipped[equipped_item_type].name == looking_item_name:
                return equipped_item
        
        for inventory_item_type in self.items.keys():
            for inventory_item_name, inventory_item in self.items[inventory_item_type].items():
                if inventory_item_name == looking_item_name:
                    return inventory_item
        
        return 0
    
    def display_spells(self):

        for spell in all_spells.__dict__.values():
            print(f"{spell.name.value} mana cost: {spell.mana_cost}", end=" | ")
        print()

    def use_spell(self, spell_name: str, target: "character"):

        # Convert string to Enum
        try:
            spell_enum = spell_Names(spell_name)
        except ValueError:
            print("Spell not found!")
            return

        spell: spell_class
        spell = SPELL_LOOKUP.get(spell_enum)
        if spell:
            # Use the spell if enough mana
            if self.mana - spell.mana_cost >= 0:
                target.HP -= spell.damage
                self.mana -= spell.mana_cost
                print(f"{self.name} did {spell.damage} damage to {target.name}")
            else: print("Not enough mana!")
        else: print("Spell not found!")

# Define mob class (inherited from character)

class mob_class(character):
    def __init__(self, name: str, attack: int, defence: int, max_HP: int, mob_type: str, mob_xp_worth: int):
        super().__init__(name, attack, defence, max_HP)
        self.mob_type = mob_type
        self.mob_xp_worth = mob_xp_worth


