SAVE_FILE = "save.txt"

def save_game(x, y):

    with open(SAVE_FILE, "w") as file:

        file.write(f"{x},{y}")

def load_game():

    try:

        with open(SAVE_FILE, "r") as file:

            data = file.read().split(",")

            return int(data[0]), int(data[1])

    except:

        return 100, 500