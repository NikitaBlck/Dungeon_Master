from characters import hero_class
from items import item_class
from DMmap import map_tile
from treasure import treasure_class
from shop import shopSizes, shopClass
import json
import copy
import inspect

from items import hero_items_empty

def init_hero_from_json(
    name: str,
    attack_attribute: int,
    defence_attribute: int,
    max_HP: int,
    HP: int,
    HP_regen: int,
    intellect: int,
    max_mana: int,
    mana: int,
    mana_regen: int,
    items: dict,
    items_equipped: dict,
    level: int,
    gold: int,
    xp: int,
    xp_until_next_lvl: int,
    pos: list,
    icon: str
) -> hero_class:

    # recreate inventory items objects from dictionary
    for key_item_types in items.keys():
        item_type_dict = dict(items.get(key_item_types))
        for key_item, value_item in item_type_dict.items():
            if value_item: items[key_item_types][key_item] = init_item_from_json(**value_item) 

    # recreate equipped items objects from dictionary
    for key, value in items_equipped.items():
        if key: items_equipped[key] = init_item_from_json(**value)

    hero = hero_class(
    name,
    attack_attribute,
    defence_attribute,
    max_HP,
    HP_regen,
    intellect,
    max_mana,
    mana_regen,
    items,
    items_equipped,
    level,
    gold,
    xp,
    xp_until_next_lvl,
    pos,
    icon)

    hero.HP = HP
    hero.mana = mana

    return hero

def init_item_from_json(name, 
                        item_type, 
                        attack_bonus, 
                        defence_bonus, 
                        max_HP_bonus, 
                        intellect_bonus, 
                        max_mana_bonus, 
                        mana_regen_bonus, 
                        gold, 
                        rarity):
    item = item_class(name=None, item_type= None, attack=0, defence=0, max_HP=0, intellect=0, max_mana=0, mana_regen=0, gold=0, rarity=None)

    item.name = name
    item.item_type = item_type 
    item.attack_bonus = attack_bonus 
    item.defence_bonus = defence_bonus
    item.max_HP_bonus = max_HP_bonus
    item.intellect_bonus = intellect_bonus
    item.max_mana_bonus = max_mana_bonus
    item.mana_regen_bonus = mana_regen_bonus
    item.gold = gold
    item.rarity = rarity

    return item

def init_treasure_from_json(gold, item) -> treasure_class:

    treasure = treasure_class()

    treasure.gold = gold
    treasure.item = item

    return treasure

def init_map_tile_from_json(biome, 
                            pos, 
                            icon, 
                            transversable, 
                            mobs_number, 
                            has_treasure,
                            treasure,
                            town_present,
                            shop,
                            message,
                            message_read) -> map_tile:

    tile = map_tile(biome, pos, icon, transversable, mobs_number, has_treasure, town_present)

    tile.treasure = treasure
    tile.shop = shop
    tile.message = message
    tile.message_read = message_read

    return tile

def read_hero_from_json() -> hero_class:
    
    with open("output.json", "r") as f:
        data = json.load(f)

    hero = init_hero_from_json(**data)
    print(hero.items)
    print(hero.items_equipped)
    print((hero.HP, hero.max_HP))
    print((hero.mana, hero.max_mana))

    return hero

def write_hero_to_json(hero: hero_class):
    hero_data = copy.deepcopy(hero.__dict__)

    # Convert item objects to dicts
    for slot, items in hero_data["items"].items():
        for item_name, item_obj in items.items():
            items[item_name] = item_obj.__dict__  # or item_obj.to_dict()
    # Converts equipped item objects to dicts
    for slot, item in hero_data["items_equipped"].items():
        hero_data["items_equipped"][slot] = item.__dict__

    with open("output.json", "w") as f:
        json.dump(hero_data, f, indent=4)

def write_game_map_to_json(game_map: list[list[map_tile]], file_name: str):
    
    map_height = len(game_map)
    map_width = len(game_map[0])
    game_map_data = list()

    # go through each tile object and turn treasure and item objects into dictionaries
    for y in range(map_height):
        row = list()
        for x in range(map_width):
            
            # Turn tile object into dictionary
            tile_temp_dict = copy.deepcopy(game_map[y][x].__dict__)
            # Turn treasure object into dictionary
            if tile_temp_dict["treasure"]:
                tile_temp_dict["treasure"] = tile_temp_dict.get("treasure").__dict__
                # if treasure has item, turn item object into dictionary
                if tile_temp_dict["treasure"]["item"]: 
                    tile_temp_dict["treasure"]["item"] = tile_temp_dict["treasure"].get('item').__dict__
                else: tile_temp_dict["treasure"]["item"] = {}
            # Turn shop object (if present) into dictionary
            if tile_temp_dict["shop"]:
                tile_temp_dict["shop"] = tile_temp_dict.get("shop").__dict__
                tile_temp_dict["shop"]["size"] = tile_temp_dict["shop"]["size"].value
            # Turn shop's items into dictionaries
                for key, value in tile_temp_dict["shop"]["items_available"].items():
                    tile_temp_dict["shop"]["items_available"][key] = value.__dict__

            row.append(tile_temp_dict)
        game_map_data.append(row)

    with open(f"{file_name}", "w") as f:
        json.dump(game_map_data, f, indent=4)

def read_game_map_from_json(file_name: str) -> list[list[map_tile]]:

    with open(f"{file_name}", "r") as f:
        game_map_data = json.load(f)
        
    map_height = len(game_map_data)
    map_width = len(game_map_data[0])

    tile_temp_dict: dict
    game_map = list()
    # create new treasure and item objects from dictionaries
    for y in range(map_height):
        row = list()
        for x in range(map_width):
            item = None
            tile_temp_dict = game_map_data[y][x]

            treasure = None
            if tile_temp_dict["treasure"]:
                # Create treasure item object
                if tile_temp_dict["treasure"]["item"]:
                    item = init_item_from_json(**tile_temp_dict["treasure"]["item"])
                    tile_temp_dict["treasure"]["item"] = item

                gold = tile_temp_dict["treasure"]["gold"]
                treasure = init_treasure_from_json(gold, item)
            # delete the treasure from dictionary to pass it separately
            del tile_temp_dict["treasure"]

            # Create shop item objects
            shop = None
            if tile_temp_dict["shop"]:
                for key, value in tile_temp_dict["shop"]["items_available"].items():
                    tile_temp_dict["shop"]["items_available"][key] = init_item_from_json(**value)
                # Create Enum for shop size
                tile_temp_dict["shop"]["size"] = shopSizes(tile_temp_dict["shop"]["size"])
                # Create shop object
                shop = shopClass.shop_from_json(tile_temp_dict["shop"])
            # delete shop object to pass it separately
            del tile_temp_dict["shop"]

            # create tile object
            tile_temp = init_map_tile_from_json(**tile_temp_dict, treasure = treasure, shop= shop)
            row.append(tile_temp)
        game_map.append(row)

    return game_map
