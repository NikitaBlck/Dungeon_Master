import random
from typing import Optional
from enum import Enum
from shop import shopClass, shopSizes
from colors_lib import colors
from characters import hero_class
from treasure import treasure_class

class biomes(Enum):

    EMPTY_BIOME = "EMPTY_BIOME"
    FOREST = "Forest"
    MOUNTAINS = "Mountains"
    SWAMP = "Swamp"
    CURSED_LAND = "Cursed land"
    MAGMA_HILLS = "Magma hills"
    BOSS_BIOME = "Boss biome"

class map_tile:
    def __init__(self, 
                 biome: str, 
                 pos: list, 
                 icon: str, 
                 transversable: bool,
                 mobs_number: int,
                 has_treasure: bool,
                 town_present: bool):
        """
        Args:
            biome (str): The biome type.
            pos (list): The position on the map.
            icon (str): The icon for the tile.
            transversable (bool): If the tile can be traversed.
            mobs_number (int): Number of mobs on the tile.
            has_treasure (bool): If the tile has treasure.
            town_present (bool): If a town is present.
        """
        self.biome = biome
        self.pos = pos
        self.icon = icon
        self.transversable = transversable
        self.mobs_number = mobs_number
        self.has_treasure = has_treasure
        self.treasure = None
        self.town_present = town_present
        self.shop = None
        self.message = []
        self.message_read = None

    def spawn_shop(self, size: Enum):
            
        self.shop = shopClass(size, self.biome, items_available={})
        self.shop.refresh_items_available()

# Function to generate a game map returns -> 2D list of map_tile objects

def generate_game_map() -> list[list[map_tile]]:
    
    map_height = 8
    map_width = 10
    game_map = list()

    for y in range(map_height):
        row = list()
        for x in range(map_width):
            # Spawn Forest on the [:][2] tiles
            if x <= 2:
                tile = map_tile(biome=biomes.FOREST.value, pos=[], transversable=True, mobs_number=1, has_treasure=True, icon="F", town_present=False)
            elif x == 3:
                # Always spawn mountain on the [0][3] tile
                if y == 0:
                    tile = map_tile(biome=biomes.MOUNTAINS.value, pos=[], transversable=False, mobs_number=0, has_treasure=False, icon="Δ", town_present=False)
                # Always spawn Forest on the [3][3] tile from the top to prevent blocking map with mountains
                elif y == 3:
                    tile = map_tile(biome=biomes.FOREST.value, pos=[], transversable=True, mobs_number=1, has_treasure=False, icon="F", town_present=False)
                else:
                # Increase chanses of mountains spawning consecutively
                    top_tile = game_map[y-1][x]
                    if top_tile.biome == biomes.MOUNTAINS.value:   
                        if random.random() < 0.6:
                            tile = map_tile(biome=biomes.MOUNTAINS.value, pos=[], transversable=False, mobs_number=0, has_treasure=False, icon="Δ", town_present=False)
                # Set standard mountain spawn chance
                    elif random.random() < 0.4:
                        tile = map_tile(biome=biomes.MOUNTAINS.value, pos=[], transversable=False, mobs_number=0, has_treasure=False, icon="Δ", town_present=False)
                # Spawn forest if mountain didn't spawn
                    else:
                        tile = map_tile(biome=biomes.FOREST.value, pos=[], transversable=True, mobs_number=1, has_treasure=False, icon="F", town_present=False)
            # Spawn swamp  on [:][4:5] tiles
            elif x == 4:
                tile = map_tile(biome=biomes.SWAMP.value, pos=[], transversable=True, mobs_number=0, has_treasure=False, icon="S", town_present=False)
            #Spawn Cursed land on [:][5:7] tiles
            elif x > 4 and x < 7:
                tile = map_tile(biome=biomes.CURSED_LAND.value, pos=[], transversable= True, mobs_number=0,has_treasure=False, icon="C", town_present=False)
            # Spawn Magma hills on [:][7:] tiles
            elif x >= 7:
                tile = map_tile(biome=biomes.MAGMA_HILLS.value, pos=[], transversable=True, mobs_number=0, has_treasure=False, icon="M", town_present=False)
            
            tile.pos = (y, x)
            row.append(tile)
        game_map.append(row)

    boss_tile = map_tile(biome=biomes.BOSS_BIOME.value, pos=[3, 9], icon="B", transversable=True, has_treasure=False, mobs_number=1, town_present=False)
    game_map[3][9] = boss_tile

    town_tile = map_tile(biome=biomes.FOREST.value, pos=[0, 0], icon="T", transversable=True, has_treasure=False, mobs_number=0, town_present=True)
    town_tile.spawn_shop(size=shopSizes.SMALL)
    game_map[0][0] = town_tile

    return game_map


# Function to draw map icons and hero

def draw_map(game_map: list[list[map_tile]], hero: hero_class) -> None:

    for y in range (len(game_map)):
        for x in range(len(game_map[0])):
            if hero.pos == list([y, x]):
                print(f"{colors.get("yellow")}{hero.icon}{colors.get("default")}", end=" ")
            else:
                map_tile_temp = game_map[y][x]
                print(map_tile_temp.icon, end=" ")
        print()

def draw_example_map(game_map: list[list[map_tile]]) -> None:
    for y in range (len(game_map)):
        for x in range(len(game_map[0])):
            map_tile_temp = game_map[y][x]
            print(map_tile_temp.icon, end=" ")
        print()

def generate_empty_map(map_height: int, map_width: int)->list[list[map_tile]]:
    
    empty_map = list()
    for y in range(map_height):
        row = list()
        for x in range(map_width):
            tile = map_tile(biome=biomes.EMPTY_BIOME.value, pos=[y, x], icon=" ",transversable=False, mobs_number=0,has_treasure=False,town_present=False)
            row.append(tile)
        empty_map.append(row)

    return empty_map
    