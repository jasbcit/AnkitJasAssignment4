import make_board
from get_user_choice import get_user_choice
from time import sleep
from enemy import Enemy
import json
import random
import make_character
from die import Die
import run_game
from colorama import Fore, Style


def clear_enemy_icon(y_coordinate, x_coordinate):
    with open("coordinates.json", "r") as file_object:
        coordinates = json.load(file_object)
    coordinates[f'{y_coordinate}:{x_coordinate}'] = "[ ]"
    with open("coordinates.json", "w") as file_object:
        json.dump(coordinates, file_object)


def second_chance(player):
    with open("character.json", "r") as file_object:
        character_dictionary = json.load(file_object)
    print()
    print("Oh no, you died... However, the House Speaker has decided to give you a second chance if you're lucky.\n")
    sleep(4)
    print(Fore.MAGENTA + "House Speaker has entered the room.\n" + Style.RESET_ALL)
    sleep(2)
    print(
        Fore.MAGENTA + player["Name"] + ", I will roll one die and then you will roll one die. If you roll higher than "
                                        "me, I will bring you back to life. Deal?" + Style.RESET_ALL)
    user_input = get_user_choice("Decision", "What do you say?", ["Roll Die", "No I'd Rather Die"])

    if user_input == "Roll Die":
        house_speaker_die = Die(20)
        house_speaker_roll = house_speaker_die.roll_die()
        print(Fore.MAGENTA + "I have rolled a " + str(house_speaker_roll) + "." + Style.RESET_ALL)
        sleep(3)
        player_die = Die(20)
        player_roll = player_die.roll_die()
        print("You rolled a " + str(player_roll) + ".")
        print()
        if player_roll > house_speaker_roll:
            print(Fore.MAGENTA + "Congratulations, I will give you your life back. Albeit at a cost..." +
                  Style.RESET_ALL)
            sleep(2)
            print(Fore.MAGENTA + "Your health has been reduced by half and you are sent back to the previous room." +
                  Style.RESET_ALL)
            print()
            sleep(3)
            character_dictionary["Current HP"] = int(character_dictionary["Current HP"] / 2)
            character_dictionary["Max HP"] = int(character_dictionary["Max HP"] / 2)
            with open("character.json", "w") as file_object:
                json.dump(character_dictionary, file_object)
            run_game.setup_current_location()
        else:
            print(Fore.MAGENTA + "Unfortunately you weren't so lucky. It was nice knowing you "
                                 "Mr.President-Who-Never-Was." + Style.RESET_ALL)
            make_character.make_character(f'{character_dictionary["Name"]}',
                                          f'{character_dictionary["Political Party"]}')
            make_board.make_board()
            quit()
    else:
        quit()


def combat_opening_interaction(enemy, player):
    with open('interactions.json') as file:
        interactions = json.load(file)

    republican_openers = [opener for value in interactions['battleOpeners'][0].values() for opener in value]
    democrat_openers = [opener for value in interactions['battleOpeners'][1].values() for opener in value]

    if player['Political Party'] == "Democrat":
        return enemy.name + ": " + republican_openers[random.randint(0, len(republican_openers) - 1)]
    elif player['Political Party'] == "Republican":
        return enemy.name + ": " + democrat_openers[random.randint(0, len(democrat_openers) - 1)]
    else:
        return "Prepare to die!"


def fight_or_leave():
    return get_user_choice('fight-or-leave', 'What would you like to do?',
                           ["Fight", "Leave"])


def roll_die(sides):
    return random.randint(1, sides - 1)


def check_health(player_hp, enemy_hp):
    with open("character.json", "r") as file_object:
        player = json.load(file_object)
    if player_hp <= 0:
        print(Fore.RED + "You died")
        second_chance(player)
        run_game.setup_current_location()
        return True
    elif enemy_hp <= 0:
        print(Fore.GREEN + "You defeated the enemy!")
        return True
    else:
        return False


def check_player_inventory(enemy, player):
    if enemy.name == "Donald Trump" or enemy.name == "Joe Biden":
        if player["Items"].count("The Constitution") >= 1:
            return True
        else:
            print(Fore.RED + enemy.name + ": You don't have The Constitution on you... You're not worth my time!" +
                  Style.RESET_ALL)
            sleep(4)
            return False

    elif enemy.name == "George W. Bush" or enemy.name == "Bernie Sanders":
        if player["Items"].count("Bald Eagle") >= 1:
            return True
        else:
            print(Fore.RED + enemy.name + ": You don't have a Bald Eagle on you... I pity your very existence!" +
                  Style.RESET_ALL)
            sleep(4)
            return False

    elif enemy.name == "Ted Cruz" or enemy.name == "Alexandria Ocasio-Cortez":
        if player["Items"].count("Presidential Pen") >= 1:
            return True
        else:
            print(Fore.RED + enemy.name + ": You don't have the Presidential Pen on you... Get out of my sight!" +
                  Style.RESET_ALL)
            sleep(4)
            return False

    else:
        return True


def check_if_level_up(player):
    player_level = player["Level"]

    if player['XP'] >= player['XP Needed to Level Up']:
        if player_level == 1:
            player['Current HP'] += 5
            player['Max HP'] += 5
        if player_level == 2:
            player['Current HP'] += 10
            player['Max HP'] += 10
        if player_level >= 3:
            player['Current HP'] += 15
            player['Max HP'] += 15
        player["Level"] += 1
        player['XP'] = 0
        player['XP Needed to Level Up'] += 5
        print(f"Congratulations, you levelled up! You now have a max HP of {player['Max HP']}.\n")
        with open("character.json", 'w') as file_object:
            json.dump(player, file_object)


def update_money_and_xp(enemy, enemy_hp, player):
    if enemy_hp <= 0 and enemy.level == 1:
        rand_xp = random.randint(1, 3)
        player['Money'] += random.randint(1, 4)
        player['XP'] += rand_xp

    if enemy_hp <= 0 and enemy.level == 2:
        player['Money'] += random.randint(4, 8)
        player['XP'] += random.randint(3, 6)

    if enemy_hp <= 0 and enemy.level == 3:
        player['Money'] += random.randint(10, 20)
        player['XP'] += random.randint(6, 10)

    with open("character.json", 'w') as file_object:
        json.dump(player, file_object)

    check_if_level_up(player)


def fight(enemy, player, difficulty):
    player_hp = player["Current HP"]
    player_attack = player["Attack Points"]
    enemy_hp = enemy.hp
    enemy_attack = enemy.attack

    if difficulty == "Easy":
        player_roll_needed = 2
        enemy_roll_needed = 8
    elif difficulty == "Medium":
        player_roll_needed = 4
        enemy_roll_needed = 4
    else:
        player_roll_needed = 8
        enemy_roll_needed = 2

    in_combat = True
    while in_combat:

        player_roll = roll_die(10)
        sleep(1)
        if player_roll >= player_roll_needed:
            enemy_hp -= player_attack
            print(Fore.GREEN + "Your hit landed!")
            if enemy_hp < 0:
                print("The enemy has 0HP left.")
            else:
                print("The enemy has " + str(enemy_hp) + "HP left.")
            print()
        else:
            enemy_hp += 0
            print(Fore.GREEN + "Your hit missed!" + Style.RESET_ALL)
            print()
        sleep(1)

        is_dead = check_health(player_hp, enemy_hp)
        if is_dead:
            print(Style.RESET_ALL)
            update_money_and_xp(enemy, enemy_hp, player)
            break

        enemy_roll = roll_die(10)
        if enemy_roll >= enemy_roll_needed:
            player_hp -= enemy_attack
            print(Fore.RED + "The enemy's hit landed!")
            if player_hp < 0:
                print("You now have 0HP left.")
            else:
                print("You now have " + str(player_hp) + "HP left.")
            print()
        else:
            player_hp += 0
            print(Fore.RED + "The enemy's hit missed!" + Style.RESET_ALL)
            print()
        sleep(1)

        is_dead = check_health(player_hp, enemy_hp)
        if is_dead:
            print(Style.RESET_ALL)
            update_money_and_xp(enemy, enemy_hp, player)
            break
    return


def combat(enemy, player, difficulty):
    is_fight_valid = check_player_inventory(enemy, player)
    if is_fight_valid:
        fight(enemy, player, difficulty)
        return
    else:
        run_game.setup_current_location()


def setup_boss():
    with open("character.json", "r+") as file_object:
        player = json.load(file_object)

    with open("character.json", "r") as file_object:
        character_dictionary = json.load(file_object)
        party = character_dictionary["Political Party"]
        dungeon_level = character_dictionary["Dungeon Level"]

    democrat_boss = ["Alexandria Ocasio-Cortez", "Bernie Sanders", "Joe Biden"]
    republican_boss = ["Ted Cruz", "George W. Bush", "Donald Trump"]
    if party == "Republican":
        boss = Enemy(democrat_boss[dungeon_level - 1], "Boss", 1 * dungeon_level, 30 * dungeon_level,
                     4 * dungeon_level)
    else:
        boss = Enemy(republican_boss[dungeon_level - 1], "Boss", 1 * dungeon_level, 30 * dungeon_level,
                     6 * dungeon_level)
    print(combat_opening_interaction(boss, player))
    print()
    user_choice = fight_or_leave()
    if user_choice == "Fight":
        combat(boss, player, "Medium")
    else:
        run_game.setup_current_location()


def setup_combat():
    with open("character.json", "r+") as file_object:
        player = json.load(file_object)

        ben_carson = Enemy("Ben Carson", "Minion", 1, 4, 1)
        sarah_palin = Enemy("Sarah Palin", "Minion", 1, 3, 1)
        mike_pence = Enemy("Mike Pence", "Minion", 1, 3, 2)

        rand_paul = Enemy("Rand Paul", "Minion", 2, 20, 4)
        arnold_schwarzenegger = Enemy("Arnold Schwarzenegger", "Minion", 2, 18, 4)
        jeb_bush = Enemy("Jeb Bush", "Minion", 2, 5, 7)

        mitt_romney = Enemy("Mitt Romney", "Minion", 3, 36, 8)
        dick_cheney = Enemy("Dick Cheney", "Minion", 3, 40, 6)
        nikki_haley = Enemy("Nikki Haley", "Minion", 3, 37, 7)

        andrew_yang = Enemy("Andrew Yang", "Minion", 1, 3, 2)
        jimmy_carter = Enemy("Jimmy Carter", "Minion", 1, 1, 1)
        kamala_harris = Enemy("Kamala Harris", "Minion", 1, 2, 3)

        beto_orourke = Enemy("Beto O'Rourke", "Minion", 2, 22, 3)
        nancy_pelosi = Enemy("Nancy Pelosi", "Minion", 2, 21, 4)
        al_gore = Enemy("Al Gore", "Minion", 2, 5, 8)

        barack_obama = Enemy("Barack Obama", "Minion", 3, 36, 8)
        hilary_clinton = Enemy("Hilary Clinton", "Minion", 3, 40, 9)
        bill_clinton = Enemy("Bill Clinton", "Minion", 3, 40, 6)

        level_one_enemies_republican = [ben_carson, sarah_palin, mike_pence]
        level_two_enemies_republican = [rand_paul, arnold_schwarzenegger, jeb_bush]
        level_three_enemies_republican = [mitt_romney, dick_cheney, nikki_haley]

        level_one_enemies_democrat = [andrew_yang, jimmy_carter, kamala_harris]
        level_two_enemies_democrat = [beto_orourke, nancy_pelosi, al_gore]
        level_three_enemies_democrat = [barack_obama, hilary_clinton, bill_clinton]

        player_political_party = player["Political Party"]
        player_level = player["Dungeon Level"]

        if player_political_party == "Republican" and player_level == 1:
            enemy = level_one_enemies_democrat[random.randint(0, 2)]
        elif player_political_party == "Republican" and player_level == 2:
            enemy = level_two_enemies_democrat[random.randint(0, 2)]
        elif player_political_party == "Republican" and player_level >= 3:
            enemy = level_three_enemies_democrat[random.randint(0, 2)]
        elif player_political_party == "Democrat" and player_level == 1:
            enemy = level_one_enemies_republican[random.randint(0, 2)]
        elif player_political_party == "Democrat" and player_level == 2:
            enemy = level_two_enemies_republican[random.randint(0, 2)]
        elif player_political_party == "Democrat" and player_level >= 3:
            enemy = level_three_enemies_republican[random.randint(0, 2)]
        else:
            enemy = mike_pence  # lol jokes
        print(combat_opening_interaction(enemy, player))
        print()
        sleep(2)
        combat(enemy, player, "Easy")


def main():
    setup_boss()


if __name__ == '__main__':
    main()
