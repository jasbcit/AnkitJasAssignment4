import json


def make_character(name, party):
    character_dictionary = {
        'Name': name,
        'X-coordinate': 2,
        'Y-coordinate': 16,
        'Dungeon Level': 1,
        'Level': 1,
        'XP': 0,
        'XP Needed to Level Up': 10,
        'Current HP': 5,
        'Max HP': 5,
        'Money': 0,
        'Attack Points': 1,
        'Visited Shop': False,
        'Achieved Goal': False,
        'Items': [],
        'Political Party': party
    }
    with open("character.json", "w") as file_object:
        json.dump(character_dictionary, file_object)

    return character_dictionary


def main():
    make_character("Ankit", party=None)


if __name__ == "__main__":
    main()
