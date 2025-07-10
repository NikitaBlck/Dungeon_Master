import keyboard
import os
import time
import copy
import shutil
from shop import shopSizes
from json_saves import write_hero_to_json, read_hero_from_json, write_game_map_to_json, read_game_map_from_json, init_item_from_json
from treasure import treasure_class
from items import all_items_dict, hero_items_empty, item_class
from DMmap import generate_game_map, draw_map, draw_example_map, generate_empty_map, map_tile, biomes
from characters import hero_class, mob_class
from colors_lib import colors

def clear():

    os.system("cls")
def displayRules():

    clear()
    example_hero = spawn_hero()
    game_map = read_game_map_from_json("map_builder.json")
    clear()
    draw_map(game_map, example_hero)

    print("Use WASD keys to move")
    print("Tiles legend:\n" \
    f"{colors.get("yellow")}{example_hero.icon}{colors.get("default")} - Hero | F - Forest | Δ - Mountains (unaccessable for hero) | S - Swamp | C - Cursed land | M - Magma hills | B - Boss\n")
    print("You need to just press the wasd keys while moving through the map, but in all other menus you need to write the key you want to press in command prompt and press enter\n")
    print("The goal of the game is to defeat boss on the boss tile")
    print("When you move through the map, on some tiles you can find different mobs")
    print("The closer you move to the boss, the stronger mobs become")
    print("You can level up your hero by gaining xp after defeating mobs")
    print("Hero restores HP and mana on level up")
    print("You can improve your hero stats by getting new gear such as armor, weapons, etc")
    print("In towns you can buy new gear in exchange for gold")
    print("You can find gold or items in treasures on some tiles\n")
    input("Press 'Enter' to continue")
def exit_the_game() -> list:
    
    clear()
#    save()
    exit(1)
def spawn_mobs(biome: str, mobs_number: int) -> mob_class:
    
    # spawn forest mobs
    if biome == biomes.FOREST.value: mob = mob_class(name="Grey wolf", attack=2 * mobs_number, defence=3, max_HP= 30 * mobs_number, mob_type="regular mob", mob_xp_worth=25 * mobs_number)
    if biome == biomes.SWAMP.value: mob = mob_class(name= "Swamp troll", attack= 4 *mobs_number, defence=5, max_HP=50 * mobs_number, mob_type="regular mob", mob_xp_worth=60 * mobs_number)
    if biome == biomes.CURSED_LAND.value: mob = mob_class(name= "Witherrot Zombie", attack= 5 *mobs_number, defence=8, max_HP=60 * mobs_number, mob_type="regular mob", mob_xp_worth=100 * mobs_number)
    if biome == biomes.MAGMA_HILLS.value: mob = mob_class(name= "Scorchwing Drake", attack= 8 *mobs_number, defence=10, max_HP=100 * mobs_number, mob_type="regular mob", mob_xp_worth=200 * mobs_number)
    if biome == "Boss biome": mob = mob_class(name="Van Darkholm", attack= 10 * mobs_number, defence=5, max_HP=200 * mobs_number, mob_type="Boss", mob_xp_worth=1000 * mobs_number)

    return mob
def spawn_hero() -> hero_class:
    hero = hero_class(name="",
                attack_attribute=10,
                defence_attribute=3,
                max_HP=100,
                HP_regen=1,
                intellect=2,
                max_mana=50,
                mana_regen=1,
                items=copy.deepcopy(hero_items_empty),
                items_equipped= {},
                level=1,
                gold=100,
                xp=0,
                xp_until_next_lvl=100,
                pos=[0, 0],
                icon="★"
                )
    return hero
def start_new_game() -> tuple[list[list[map_tile]], hero_class]:
    clear()
    hero = spawn_hero()
    hero.name = input("Your name is: ")
    clear()
    return read_game_map_from_json("map_builder.json"), hero
def enter_shop(tile: map_tile, hero: hero_class):

    while True:
        print("You have entered a shop")
        tile.shop.display_items_available()
        print(f"{hero.name}'s gold: {hero.gold}")
        hero.print_inventory()
        print("1. Go back | 2. Buy item")
        shop_menu_choice = input("\n")

        if shop_menu_choice == "1":
            break
        elif shop_menu_choice == "2":
            print("Type the exact name of the item like 'Elven Bow', 'Silver Band', etc ")
            item_can_be_sold = tile.shop.sell_item(input(), hero)
            if item_can_be_sold:
                hero.buy_item(item_can_be_sold)
        clear()
def menu() -> str:

    clear()

    print(f"{colors.get("yellow")}🔥Dungeon Master🔥{colors.get("default")}\n")
    print("1. New game")
    print("2. Continue game")
    print("3. Load game")
    print("4. Save game")
    print("5. Build new map")
    print("6. Load map builder")
    print("7. Rules")
    print("8. Exit\n")
    return input()
def battle(game_map: list[list[map_tile]], hero: hero_class) -> bool:

    hero_HP_pre_battle = hero.HP
    hero_mana_pre_battle = hero.mana

    drank_potion_name = None
    tile_temp: map_tile = game_map[hero.pos[0]][hero.pos[1]]
    mob = spawn_mobs(tile_temp.biome, tile_temp.mobs_number)

    # give some delay before the battle starts

    print("battle loading...")
    time.sleep(0.3)

    while mob.HP > 0:

        clear()
        print(f"You have discovered a {mob.name} lair")
        print(f"A {mob.name} (x{tile_temp.mobs_number}) rushes towards you")
        print(f"{hero.name}'s HP:{hero.HP} | mana: {hero.mana}")
        print(f"{mob.name}'s HP:{mob.HP}")
        user_choice = input("1. Attack | 2. Drink potion | 3. Use spell\n")

        if user_choice == "1":
            hero.attack(mob)
            mob.attack(hero)
            time.sleep(0.8)
        elif user_choice == "2":
            try:
                if hero.items_equipped:
                    if hero.items_equipped["potions"]:
                        drank_potion_name = hero.drink_potion()
                        del hero.items_equipped["potions"]
                    else:
                        print("No potions equipped")
                        time.sleep(1.5)
                else:
                    print("No potions equipped")
                    time.sleep(1.5)
            except:
                print("No potions equiped")
                time.sleep(1.5)
        elif user_choice == "3":
            hero.display_spells()
            hero.use_spell(input("Enter spell to cast: "), mob)
            time.sleep(1)

        # Check if hero has died, return true if yes
        if hero.HP <= 0:
            clear()
            hero.hero_death()
            return True
    
    clear()

    tile_temp.mobs_number = 0
    tile_temp.icon = "o"
    
    # Add experience for the battle
    print(f"You have defeated the {mob.name}")
    print(f"xp gained: {mob.mob_xp_worth}")
    hero.xp += mob.mob_xp_worth

    # reset potion effects after battle
    hero.reset_potion_effects(drank_potion_name)

    # restore after battle
    hero.restore_after_battle(hero_HP_pre_battle, hero_mana_pre_battle)

    time.sleep(1.5)

    clear()
def build_map(map_for_build: list[list[map_tile]]) -> list[list[map_tile]]:

    clear()

    map_builder_hero = spawn_hero()

    while True:

        tile_temp = map_for_build[map_builder_hero.pos[0]][map_builder_hero.pos[1]]

        while True:

            clear()

            draw_map(map_for_build, map_builder_hero)

            print("Press to change :\n"
            "1. biome | 2. transversability | 3. mobs number | 4. treasure | 5. town | 6. message")
            print(f"Biome: {tile_temp.biome}")
            print(f"Transversable: {tile_temp.transversable}")
            print(f"Mobs: {tile_temp.mobs_number}")
            print(f"Treasure: {tile_temp.has_treasure}")
            if tile_temp.treasure:
                print(f"Treasure gold: {tile_temp.treasure.gold}")
                if tile_temp.treasure.item: print(f"Treasure item: {tile_temp.treasure.item.name}")
            print(f"Town: {tile_temp.town_present}")
            print(f"Tile message: {tile_temp.message}")
            print(f"Message read: {tile_temp.message_read}")

            #event = keyboard.read_event()
            #if event.event_type == "down":
                #key = event.name

            key = input()

            match key:
                # going back to menu
                case 'esc':
                    return map_for_build
                # hero movement with going out of map limit constraints
                case 'w':
                    map_builder_hero.pos[0] = max(0, map_builder_hero.pos[0] - 1)
                    break
                case 'a':
                    map_builder_hero.pos[1] = max(0, map_builder_hero.pos[1] - 1)
                    break
                case 's':
                    map_builder_hero.pos[0] = min(len(map_for_build) - 1, map_builder_hero.pos[0] + 1)
                    break
                case 'd':
                    map_builder_hero.pos[1] = min(len(map_for_build[0]) - 1, map_builder_hero.pos[1] + 1)
                    break

            # map building features

                # changing biome
                case '1':
                    print("Enter:")
                    print("'1' - Forest | '2' - Mountains | '3' - Swamp | '4' - Cursed land | '5' - Magma hills | '6' - Boss biome | '7' - Empty")
                    biome_choice = input()
                    match biome_choice:
                        case '1': 
                            tile_temp.biome = biomes.FOREST.value
                            tile_temp.icon = "F"
                            tile_temp.transversable = True
                        case '2':
                            tile_temp.biome = biomes.MOUNTAINS.value
                            tile_temp.icon = "Δ"
                            tile_temp.transversable = False
                        case '3':
                            tile_temp.biome = biomes.SWAMP.value
                            tile_temp.icon = "S"
                            tile_temp.transversable = True
                        case '4':
                            tile_temp.biome = biomes.CURSED_LAND.value
                            tile_temp.icon = "C"
                            tile_temp.transversable = True
                        case '5':
                            tile_temp.biome = biomes.MAGMA_HILLS.value
                            tile_temp.icon = "M"
                            tile_temp.transversable = True
                        case '6':
                            tile_temp.biome = biomes.BOSS_BIOME.value
                            tile_temp.icon = "B"
                            tile_temp.transversable = True
                        case '7': 
                            tile_temp.biome = biomes.EMPTY_BIOME.value
                            tile_temp.icon = " "
                            tile_temp.transversable = False
                            tile_temp.mobs_number = 0
                            tile_temp.has_treasure = False
                            tile_temp.town_present = False
                            tile_temp.shop = None
                            tile_temp.message_read = None
                        case _:
                            print("Invalid biome choice.")
                            time.sleep(1)
                    break
                # changing transversability
                case '2':
                    print("Enter 1. transversable | 2. non-transversable")
                    transversable_choice = input()
                    if transversable_choice == "1": tile_temp.transversable = True
                    elif transversable_choice == "2": tile_temp.transversable = False
                    else:
                        print("Wrong input")
                        time.sleep(1)
                    break
                # changing mobs number on the tile
                case '3':
                    print("Enter number of mobs to spawn on the tile:")
                    try:
                        tile_temp.mobs_number = int(input())
                    except:
                        print("Wrong input")
                        time.sleep(1)
                    break
                # changing treasure availability
                case '4':
                    print("Enter 1. treasure | 2. no treasure")
                    treasure_choice = input()
                    if treasure_choice == "1": 
                        tile_temp.has_treasure = True
                        tile_temp.treasure = treasure_class()
                        print("Enter 1. gold treasure | 2. item treasure")
                        gold_item_choice = input("\n")
                        if gold_item_choice == "1":
                            try:
                                gold_in_chest = int(input("Enter how amount of gold in chest: "))
                                tile_temp.treasure.gold = gold_in_chest
                            except:
                                print("Wrong input")
                                time.sleep(1.5)
                        elif gold_item_choice == "2":
                            item_name = input("Enter item's name: ")
                            tile_temp.treasure.item = item_class.item_from_name(item_name)
                        else:
                            print("Wrong input")
                            time.sleep(1)
                    elif treasure_choice == "2":
                        tile_temp.has_treasure = False
                        tile_temp.treasure = None
                    else:
                        print("Wrong input")
                        time.sleep(1)
                    break
                # Placing town
                case '5':
                    if tile_temp.biome != biomes.EMPTY_BIOME.value:
                        print("Enter 1. town | 2. no town")
                        town_choice = input()
                        if town_choice == "1": 
                            tile_temp.town_present = True
                            print("Select shop size 1. small | 2. medium | 3. large")
                            shop_size_choice = input()
                            try:
                                if shop_size_choice == "1": tile_temp.spawn_shop(shopSizes.SMALL)
                                elif shop_size_choice == "2": tile_temp.spawn_shop(shopSizes.MEDIUM)
                                elif shop_size_choice == "3": tile_temp.spawn_shop(shopSizes.LARGE)
                                else:
                                    print("Wrong data")
                                    time.sleep(1)
                            except:
                                print("something went wrong")
                                time.sleep(2)

                        elif town_choice == "2": tile_temp.town_present = False
                        else:
                            print("Wrong input")
                            time.sleep(1)
                    else:
                        print("Select biome first")
                        time.sleep(1)
                case '6':
                    print("1. Add new message | 2. Edit message | 3. Delete message")
                    user_message_choice = input()
                    match user_message_choice:
                        case '1':
                            tile_temp.message.append(input("Print new message: "))
                            tile_temp.message_read = False
                            print()
                        case '2':
                            try:
                                message_number_to_edit = int(input("Enter number of message to edit: "))
                                if tile_temp.message[message_number_to_edit]:
                                    tile_temp.message[message_number_to_edit] = input("\nEnter the message: ")
                                    print()
                            except:
                                print("Message doesn't exist")
                                time.sleep(2)
                        case '3':
                            try:
                                del tile_temp.message[int(input("Enter number of message to delete: "))]
                                if tile_temp.message == []:
                                    tile_temp.message_read = None
                            except:
                                print("Message doesn't exist")
                                time.sleep(2)
                case _:
                    print("Wrong input")
                    time.sleep(1)
                    break

            # if tile has town, change icon to "T"
            if tile_temp.town_present:
                tile_temp.icon = "T"
def save_builder_map(map_for_save: list[list[map_tile]]):
    while True:
    
        clear()
        print("Press 1. Save map | 2. Discard map")
        user_choice = input()
        if user_choice == "1":
            write_game_map_to_json(map_for_save, "map_builder.json")
            break
        elif user_choice == "2":
            break
        else: continue
def play(game_map: list[list[map_tile]], hero: hero_class) -> tuple[list, bool]:

    game_finished = False

    while True:
        clear()

        # start battle if mobs found on the tile
        tile_temp = game_map[hero.pos[0]][hero.pos[1]]
        if tile_temp.mobs_number > 0:
            # if hero died battle() returns True
            if battle(game_map, hero): # enter battle
                continue
        
        # print messages
        if tile_temp.message and tile_temp.message_read == False:
            for message in tile_temp.message:
                clear()
                print(message)
                input("Press 'Enter' to continue...\n")
            tile_temp.message_read = True
            clear()
        
        # if killed boss, finish the game
        if tile_temp.biome == "Boss biome" and tile_temp.mobs_number == 0:
            print("Congratulations!!! You have finished the game!")
            game_finished = True
            time.sleep(5)
            return game_map, game_finished
            
        # pick up treasure if it is present on the tile
        if tile_temp.has_treasure == True and tile_temp.mobs_number == 0:
            hero.pick_up_treasure(tile_temp.treasure.gold, tile_temp.treasure.item)
            input("\nPress 'Enter' to continue")
        # remove treasure from the tile
            tile_temp.has_treasure = False
            clear()

        # Check if player can level up
        if hero.xp >= hero.xp_until_next_lvl:
            hero.level_up()
            clear()

        # draw UI
        print(f"Level: {hero.level} | Gold: {hero.gold} | HP: {hero.HP}/{hero.max_HP}")

        # refresh map
        draw_map(game_map, hero)

        # draw UI
        print("Esc - Menu | C - Character | I - Inventory", end = "")
        if tile_temp.town_present: print(" | E - Enter Shop")
        print()

        # Hero controls
        previous_hero_pos = tuple(hero.pos)
        while True:
            
            event = keyboard.read_event()
            if event.event_type == "down":
                key = event.name

                match key:
                    # going back to menu
                    case 'esc':
                        return game_map, game_finished
                    # hero movement with going out of map limit constraints
                    case 'w':
                        hero.pos[0] = max(0, hero.pos[0] - 1)
                        break
                    case 'a':
                        hero.pos[1] = max(0, hero.pos[1] - 1)
                        break
                    case 's':
                        hero.pos[0] = min(len(game_map) - 1, hero.pos[0] + 1)
                        break
                    case 'd':
                        hero.pos[1] = min(len(game_map[0]) - 1, hero.pos[1] + 1)
                        break
                    # Display hero stats
                    case 'c':
                        clear()
                        print(f"{hero.name}\n"
                              f"Level: {hero.level} ({hero.xp}/{hero.xp_until_next_lvl})\n"
                              f"Gold: {hero.gold}\n"
                              f"Attack: {hero.attack_attribute}\n"
                              f"Defence: {hero.defence_attribute}\n"
                              f"Intellect: {hero.intellect}\n"
                              f"HP: {hero.HP}/{hero.max_HP}\n"
                              f"HP regen: {hero.HP_regen}\n"
                              f"Mana: {hero.mana}/{hero.max_mana}\n"
                              f"Mana regen: {hero.mana_regen}\n"
                              )
                        # Press esc to go back to the map
                        print("← 'Esc'")
                        while True:
                            event = keyboard.read_event()
                            if event.event_type == "down":
                                exit_character_stats_key = event.name
                                if exit_character_stats_key == "esc":
                                    break
                        break
                    case 'i':
                        while True:
                            clear()
                            hero.print_equipped()
                            hero.print_inventory()
                            inventory_choice = input("\n 1. Go back | 2. Equip item | 3. Drop equipped item | 4. Item info\n")
                            if inventory_choice == "1":
                                break
                            elif inventory_choice == "2":
                                print("Type the exact name of the item like 'Elven Bow', 'Silver Band', etc ")
                                hero.equip_item(input("Item to equip: "))
                            elif inventory_choice == "3":
                                print("Type the exact TYPE of equipment you want to drop like 'weapon', 'ring', etc ")
                                hero.drop_item(input("Equipment to drop: "))
                            elif inventory_choice == "4":
                                print("Type the exact name of the item like 'Elven Bow', 'Silver Band', etc ")
                                print()
                                found_item = hero.find_item(input())
                                if found_item:
                                    found_item.display_item_stats()
                                    input("\nPress 'enter' to continue")

                        break
                    case 'e':
                        if tile_temp.town_present:
                            clear()
                            enter_shop(tile_temp, hero)
                            clear()
                        break
                    case _:
                        continue

        # if player tries to cross the mountains, teleport him to previous position
        tile_temp = game_map[hero.pos[0]][hero.pos[1]]
        if tile_temp.transversable == False:
            hero.pos = list(previous_hero_pos)
def main():

    game_running = False
    game_finished = False
    while True:
        menu_choice = menu()

        if menu_choice == "1":
            
            displayRules()
            game_map, hero = start_new_game()
            game_running = True
            game_map, game_finished = play(game_map, hero)

        if menu_choice =="2":
            if game_running == True:
                game_map, game_finished = play(game_map, hero)
            else:
                print("No game currently running")
                time.sleep(1.5)

        if menu_choice == "3":
            try:
                game_map = read_game_map_from_json("output_map.json")
                hero = read_hero_from_json()
            except:
                print("Possibly, there was no file to be read")
                time.sleep(2)
                continue
            game_running = True
            game_map, game_finished = play(game_map, hero)
        
        if menu_choice == "4":
            if game_running: 
                write_hero_to_json(hero)
                write_game_map_to_json(game_map, "output_map.json")
            else:
                print("No game currently running")
                time.sleep(1.5)
        
        if menu_choice == "5":

            map_for_build = generate_empty_map(8, 15)
            map_for_save = build_map(map_for_build)

            save_builder_map(map_for_save)

        if menu_choice == "6":

            try:
                map_for_save = build_map(read_game_map_from_json("map_builder.json"))
                save_builder_map(map_for_save)
            except:
                print("Couldn't find appropriate file to read")
                time.sleep(2)
                continue

        if menu_choice == "7":
            displayRules()

        if menu_choice == "8":
            exit_the_game()

            # QUICK TESTS MENU #DONT FORGET TO DELETE!!!
        if menu_choice == "9":
            game_map, hero = start_new_game()
            write_game_map_to_json(game_map)
            input()
            read_game_map_from_json()

        if game_finished == True: game_running = False

if __name__ == "__main__":
    main()