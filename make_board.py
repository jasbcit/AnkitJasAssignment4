import json
from describe_current_location import check_for_random_enemy
from shopkeeper import setup_shopkeeper
from combat import setup_combat
def make_events():
    with open("event.json", "w") as file_object:
        event_dictionary = {"   ": None,
                            "[ ]": check_for_random_enemy(),
                            "[S]": setup_shopkeeper(),
                            "[B]": setup_combat(),
                            "[E]": setup_combat(),
                            "!": "[!]",
                            "?": "[?]",
                            "K": "[K]",
                            "[o]": None
                            }
        json.dump(event_dictionary, file_object)
def make_board():
    icons = {
        "0": "   ",
        "1": "[ ]",
        "S": "[S]",
        "B": "[B]",
        "E": "[E]",
        "!": "[!]",
        "?": "[?]",
        "K": "[K]",
        "o": "[o]"
    }
    with open("white_house.txt", 'r') as white_house_map:
        coordinates = {}
        board = white_house_map.readlines()
        for index_row, row in enumerate(board):
            for index_room, room in enumerate(row):
                if room != "\n":
                    coordinates[f'{index_row}:{index_room}'] = icons.get(room)
        with open("coordinates.json", "w") as file_object:
            json.dump(coordinates, file_object)


def main():
    make_board()


if __name__ == "__main__":
    main()
