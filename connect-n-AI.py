from math import sqrt
import numpy as np
import random as rdm
import pickle
import arcade

def make_field(n):
    field = []
    internalfield = []
    for i in range(n):
        internalfield.append(".")

    while n > 0:
        field.append(internalfield)
        n -= 1

    matrix = np.matrix(field)
    return matrix

def check(player, matrix, x, y):
    return (player == "o" or player == "x") and x < sqrt(matrix.size) and y < sqrt(matrix.size) and matrix[y,x] == "."

def place(player, matrix, x, y):
    if check(player, matrix, x, y):
        matrix[y,x] = player

def full(matrix):
    if "." in matrix:
        return False
    else:
        return True

def winner(matrix):
    winner = check_horizontal(matrix)
    if winner == 0:
        winner = check_vertical(matrix)
        if winner == 0:
            winner = check_diagonal(matrix)
            if winner == 0 and full(matrix):
                winner = 1
    return winner

def check_horizontal(matrix):
    size = int(sqrt(matrix.size))
    for y in range(size):
        for x in range(size):
            if(matrix[y,x] == "o" and x+2 < size and matrix[y,x+1] == "o" and matrix[y,x+2] == "o"):
                return "o"
            elif(matrix[y,x] == "x" and x+2 < size and matrix[y,x+1] == "x" and matrix[y,x+2] == "x"):
                return "x"
    return 0

def check_vertical(matrix):
    size = int(sqrt(matrix.size))
    for x in range(size):
        for y in range(size):
            if(matrix[y,x] == "o" and y+2 < size and matrix[y+1,x] == "o" and matrix[y+2,x] == "o"):
                return "o"
            elif(matrix[y,x] == "x" and y+2 < size and matrix[y+1,x] == "x" and matrix[y+2,x] == "x"):
                return "x"
    return 0

def check_diagonal(matrix):
    size = int(sqrt(matrix.size))
    diagonalen = []
    for i in range(size):
        diag = np.diagonal(matrix, i)
        mindiag = np.diagonal(matrix, -i)
        contradiag = np.diagonal(np.fliplr(matrix), i)
        mincontradiag = np.diagonal(np.fliplr(matrix), -i)
        if size <= diag.size:
            diagonalen.append(list(diag))
            diagonalen.append(list(mindiag))
            diagonalen.append(list(contradiag))
            diagonalen.append(list(mincontradiag))

    for diagonaal in diagonalen:
        length = len(diagonaal)
        for i in range(length):
            if diagonaal[i] == "o" and i+2 < length and diagonaal[i+1] == "o" and diagonaal[i+2] == "o":
                return "o"
            elif diagonaal[i] == "x" and i+2 < length and diagonaal[i+1] == "x" and diagonaal[i+2] == "x":
                return "x"
    return 0

def gameloop(matrix, player1, player2, playmode=0):
    SAQ_file = open(r"C:/Users/seppe/OneDrive - Melios/Seppe/Hobby's/Project AI/SAQ_file.pkl", "rb")
    SAQ = pickle.load(SAQ_file)
    SAQ_file.close()

    while(winner(matrix) == 0 and winner(matrix) != 1):
        xco = int(input(player1 + ", give x-co: "))
        yco = int(input(player1 + ", give y-co: "))

        while not check("x", matrix, xco, yco):
            print("Those coördinates are not valid, try again")
            xco = int(input(player1 + ", give x-co: "))
            yco = int(input(player1 + ", give y-co: "))

        place("x", matrix, xco, yco)
        print(matrix)

        if(winner(matrix) == 0 and winner(matrix) != 1):
            if playmode == 0:
                xco = int(input(player2 + ", give x-co: "))
                yco = int(input(player2 + ", give y-co: "))

                while not check("o", matrix, xco, yco):
                    print("Those coördinates are not valid, try again")
                    xco = int(input(player2 + ", give x-co: "))
                    yco = int(input(player2 + ", give y-co: "))

                place("o", matrix, xco, yco)
                print(matrix)
            else:
                computedAI("o", matrix, SAQ, {})
                print(matrix)

    if(winner(matrix) != 1):
        if(winner(matrix) == "o"):
            print(player2 + " has won the game!")
        else:
            print(player1 + " has won the game!")
    else:
        print("It's a draw")

    again = input("Again? ")

    if "ye" in again:
        gameloop(make_field(int(sqrt(matrix.size))), player1, player2, playmode)

def UI():
    print("What do you want to do?")
    print("0: train AI \n"
          "1: play Tic Tac Toe \n"
          "2: see data of the AI \n")

    choice = int(input("Make your choice: "))

    if choice == 0:
        dim = int(input("Dimension: "))
        time = int(input("Time: "))
        training_type = input("Train against: 0) random opponent \n"
                              "               1) determined opponent \n"
                              "Make your choice: ")

        SAQ_type = input("Do you want to save the training results in a file? ")

        if "ye" in SAQ_type:
            file = input("Where do you want to save the training results? ")
            Training(dim, time, 1, training_type, file)
            print("Training completed...")
        else:
            Training(dim, time, 0, training_type)
            print("Training completed...")

    elif choice == 1:
        print("----- NEW Tic Tac Toe Game ------ \n")
        size = int(input("Field size: "))
        cvp_or_pvp = input("Do you want to play against the computer? ")
        if "ye" in cvp_or_pvp:
            Player1 = input("What is your name? ")
            field = make_field(size)
            print("Let the game begin")
            print("You are x, the AI is o")
            gameloop(field, Player1, "AI", 1)

        else:
            Player1 = input("Name of first player: ")
            Player2 = input("Name of second player: ")
            field = make_field(size)

            print("Let the game begin")
            print(Player1 + " is x, " + Player2 + " is o")
            gameloop(field, Player1, Player2)

    elif choice == 2:
        file = input("Give the file-name of the AI data: ")
        SAQ_file = open(file, "rb")
        SAQ = pickle.load(SAQ_file)
        SAQ_file.close()
        print(SAQ)

def update_SAQ(SAQ, state, action, Q):
    if state in SAQ:
        SAQ[state].update({action: Q})
    else:
        SAQ.update({state: {action: Q}})

def update_Q(SAQ, state, action, R, next_Q):
   if state in SAQ and action in SAQ[state].keys():
       return 0.6*SAQ[state][action] + 0.4*(R + 0.9*next_Q)
   else:
       return 0.4*R + 0.36*next_Q

def fill_SAQ(SAQ, winning_AI, losing_AI, draw=0):
    winning_AI = list(winning_AI.items())
    losing_AI = list(losing_AI.items())
    x = len(winning_AI)-1
    y = len(losing_AI)-1
    if draw == 0:
        R = 1
        next_winning_Q = 0
        next_losing_Q = 0
        while x >= 0:
            winning_state = winning_AI[x][0]
            winning_action = tuple(winning_AI[x][1].keys())[0]
            losing_state = losing_AI[y][0]
            losing_action = tuple(losing_AI[y][1].keys())[0]

            winning_Q = update_Q(SAQ, winning_state, winning_action, R, next_winning_Q)
            losing_Q = update_Q(SAQ, losing_state, losing_action, -R, next_losing_Q)

            next_winning_Q = winning_Q
            next_losing_Q = losing_Q

            update_SAQ(SAQ, winning_state, winning_action, winning_Q)
            update_SAQ(SAQ, losing_state, losing_action, losing_Q)
            x -= 1
            y -= 1
            R = 0
    else:
        while x >= 0:
            update_SAQ(SAQ, winning_AI[x][0], tuple(winning_AI[x][1].keys())[0], 0)
            update_SAQ(SAQ, losing_AI[y][0], tuple(losing_AI[y][1].keys())[0], 0)
            x -= 1
            y -= 1

def state_toString(state):
    newstate = state.tolist()
    string = ""
    for x in newstate:
        for y in x:
            string = string + y
    return string

def getPossibleActions(field):
    actionlist = []
    dim = int(sqrt(field.size))
    for y in range(dim):
        for x in range(dim):
            if field[y,x] == ".":
                actionlist.append((x, y))
    return actionlist

def computedAI(player, field, SAQ, gameSAQ):
    newfield = state_toString(field)
    if newfield in SAQ.keys():
        best_action = max(SAQ[newfield], key=lambda key: SAQ[newfield][key])
        place(player, field, best_action[0], best_action[1])
        update_SAQ(gameSAQ, newfield, best_action, 0)
    else:
        randomAI(player, field, gameSAQ)

def randomAI(player, field, gameSAQ):
    actions = getPossibleActions(field)
    choice = rdm.randrange(0, len(actions))
    xco = actions[choice][0]
    yco = actions[choice][1]

    update_SAQ(gameSAQ, state_toString(field), (xco, yco), 0)
    place(player, field, xco, yco)

def determined_player(player, field, gameSAQ):
    possible_actions = getPossibleActions(field)
    x = 0
    test_field = field.copy()
    while x in range(len(possible_actions)) and winner(test_field) != "x":
        test_field = field.copy()
        place(player, test_field, possible_actions[x][0], possible_actions[x][1])
        x += 1

    if(winner(test_field) == "x"):
        update_SAQ(gameSAQ, state_toString(field), (possible_actions[x-1][0], possible_actions[x-1][1]), 0)
        place(player, field, possible_actions[x-1][0], possible_actions[x-1][1])
    else:
        x = 0
        test_field = field.copy()
        while x in range(len(possible_actions)) and winner(test_field) != "o":
            test_field = field.copy()
            place("o", test_field, possible_actions[x][0], possible_actions[x][1])
            x += 1

        if (winner(test_field) == "o"):
            update_SAQ(gameSAQ, state_toString(field), (possible_actions[x - 1][0], possible_actions[x - 1][1]), 0)
            place(player, field, possible_actions[x - 1][0], possible_actions[x - 1][1])
        else:
            randomAI(player, field, gameSAQ)

def Training(dim, time, SAQ_type, powertraining, file=None):

    if SAQ_type == 0:
        SAQ = {}
    else:
        SAQ_file = open(file, "rb")
        SAQ = pickle.load(SAQ_file)
        SAQ_file.close()

    draw = 0
    for i in range(time):
        field = make_field(dim)
        gameSAQ_O = {}
        gameSAQ_X = {}
        x = 0
        while(winner(field) == 0 and winner(field) != 1):
            rorc = rdm.randrange(0,100,1)
            player = "x" if x % 2 == 0 else "o"
            if(player == "o"):
                if rorc < 30:
                    computedAI(player, field, SAQ, gameSAQ_O)
                else:
                    randomAI(player, field, gameSAQ_O)
            else:
                if powertraining:
                    determined_player(player, field, gameSAQ_X)
                else:
                    randomAI(player, field, gameSAQ_X)
            x += 1

        if (winner(field) != 1):
            if (winner(field) == "o"):
                fill_SAQ(SAQ, gameSAQ_O, gameSAQ_X)
            else:
                fill_SAQ(SAQ, gameSAQ_X, gameSAQ_O)
        else:
            draw += 1
            fill_SAQ(SAQ, gameSAQ_O, gameSAQ_X, 1)

    if SAQ_type != 0:
        SAQ_file = open(file, "wb")
        pickle.dump(SAQ, SAQ_file)
        SAQ_file.close()

def image_field(field):
    dim = int(sqrt(field.size))
    square_dim = 700/dim
    radius = (square_dim/2)-10

    arcade.draw_lrtb_rectangle_outline(50, 750, 750, 50, arcade.color.BLACK)

    for x in range(1, dim):
        arcade.draw_line_strip([[50 + square_dim*x, 750], [50 + square_dim*x, 50]], arcade.color.BLACK)
        arcade.draw_line_strip([[50, 750-square_dim*x], [750, 750-square_dim*x]], arcade.color.BLACK)

    for y in range(dim):
        for x in range(dim):
            if field[y, x] == "x":
                place_symbol("x", 50 + square_dim*(x + 0.5), 750 - square_dim*(y + 0.5), radius)
            elif field[y, x] == "o":
                place_symbol("o", 50 + square_dim*(x + 0.5), 750 - square_dim*(y + 0.5), radius)

def place_symbol(symbol, x, y, radius):

    if symbol == "o":
        arcade.draw_circle_outline(x, y, radius, arcade.color.BLACK)
    elif symbol == "x":
        l = radius/sqrt(2)
        left = x-l
        right = x+l
        up = y+l
        down = y-l
        arcade.draw_line_strip([[left, up], [right, down]], arcade.color.BLACK)
        arcade.draw_line_strip([[left, down], [right, up]], arcade.color.BLACK)

def find_coordinates(size, x, y):
    square_dim = 700/size

    for i in range(size):
        for j in range(size):
            if 50 + square_dim*i < x <= 50 + square_dim*(i+1) and 750-square_dim*(j+1) < y <= 750-square_dim*j:
                return tuple([i, j])
    return None

def MainMenuButton():
    arcade.draw_lrtb_rectangle_filled(700, 790, 800, 760, arcade.color.BLUE)
    arcade.draw_text("Home", 710, 780, arcade.color.WHITE)

def MainMenuMech(x, y, window):
    if 700 < x < 790 and 760 < y < 800:
        Main_menu = MainMenu()
        window.show_view(Main_menu)

class MainMenu(arcade.View):

    def __init__(self):
        super().__init__()

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_lrtb_rectangle_filled(200, 600, 710, 510, arcade.color.AERO_BLUE)
        arcade.draw_lrtb_rectangle_filled(200, 600, 500, 300, arcade.color.AERO_BLUE)
        arcade.draw_text("Play Tic Tac Toe", 400, 610, arcade.color.RUBY_RED, 20, 0, "left", "calibri", False, False,
                         "center")
        arcade.draw_text("Train AI", 400, 400, arcade.color.RUBY_RED, 20, 0, "left", "calibri", False, False,
                     "center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if 200 < x < 600:
            if 510 < y < 710:
                TTT_menu = TTTmenu(0)
                self.window.show_view(TTT_menu)

            elif 300 < y < 500:
                Train_AI = TTTmenu(1)
                self.window.show_view(Train_AI)

class TTTmenu(arcade.View):

    def __init__(self, play_or_train):
        super().__init__()
        self.fieldsize = ""
        self.play_or_train = play_or_train

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Choose fieldsize:", 200, 715, arcade.color.WHITE)
        arcade.draw_lrtb_rectangle_filled(200, 240, 710, 610, arcade.color.WHITE)
        arcade.draw_text("3", 210, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(250, 290, 710, 610, arcade.color.WHITE)
        arcade.draw_text("4", 260, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(300, 340, 710, 610, arcade.color.WHITE)
        arcade.draw_text("5", 310, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(350, 390, 710, 610, arcade.color.WHITE)
        arcade.draw_text("6", 360, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(400, 440, 710, 610, arcade.color.WHITE)
        arcade.draw_text("7", 410, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(450, 490, 710, 610, arcade.color.WHITE)
        arcade.draw_text("8", 460, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(500, 540, 710, 610, arcade.color.WHITE)
        arcade.draw_text("9", 510, 660, arcade.color.RUBY_RED)
        arcade.draw_lrtb_rectangle_filled(550, 590, 710, 610, arcade.color.WHITE)
        arcade.draw_text("10", 560, 660, arcade.color.RUBY_RED)
        MainMenuButton()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if 610 < y < 710:
            for i in range(8):
                if 200 + 50*i < x < 240 + 50*i:
                    if self.play_or_train == 0:
                        new_game = MyGame(i+3)
                        self.window.show_view(new_game)
                    else:
                        new_training = TrainingMenu(i+3)
                        self.window.show_view(new_training)

        MainMenuMech(x, y, self.window)

class TrainingMenu(arcade.View):

    def __init__(self, dim):
        super().__init__()
        self.dim = dim
        self.trained = 0

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        arcade.draw_lrtb_rectangle_filled(200,600,500,300, arcade.color.WHITE)
        arcade.draw_text(
            "Start Training",
            400,
            400,
            arcade.color.RUBY_RED,
            30,
            anchor_x="center",
        )
        MainMenuButton()

        if self.trained > 0:
            arcade.draw_text(
                "Trained for " + str(self.trained) + " iterations on " + str(self.dim) + "x" + str(self.dim),
                200,
                510,
                arcade.color.WHITE,
                20,
            )

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        Training(self.dim, 100, 1, True, r"C:/Users/seppe/OneDrive - Melios/Seppe/Hobby's/Project AI/SAQ_file.pkl")
        self.trained += 100

        MainMenuMech(x, y, self.window)

class MyGame(arcade.View):

    def __init__(self, fieldsize):
        super().__init__()
        self.fieldsize = fieldsize
        self.field = None
        self.turn = None
        self.SAQ = None
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.field = make_field(self.fieldsize)
        self.turn = "p1"
        SAQ_file = open(r"C:/Users/seppe/OneDrive - Melios/Seppe/Hobby's/Project AI/SAQ_file.pkl", "rb")
        self.SAQ = pickle.load(SAQ_file)
        SAQ_file.close()

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """Render the screen."""
        self.clear()
        image_field(self.field)
        MainMenuButton()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        coordinates = find_coordinates(self.fieldsize, x, y)

        if coordinates is not None and check("x", self.field, coordinates[0], coordinates[1]) and self.turn == "p1":
            place("x", self.field, coordinates[0], coordinates[1])
            if winner(self.field) == "x" or winner(self.field) == 1:
                self.turn = ""
                game_over = GameOverView(winner(self.field), self.fieldsize)
                self.window.show_view(game_over)

            else:
                self.turn = "AI"
                computedAI("o", self.field, self.SAQ, {})
                if winner(self.field) == "o" or winner(self.field) == 1:
                    self.turn = ""
                    last_move_view = LastMoveView(self.field, self.fieldsize)
                    self.window.show_view(last_move_view)
                else:
                    self.turn = "p1"

        MainMenuMech(x, y, self.window)

class LastMoveView(arcade.View):
    def __init__(self, field, fieldsize):
        super().__init__()
        self.field = field
        self.fieldsize = fieldsize

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        image_field(self.field)
        MainMenuButton()

    def on_mouse_press(self, x, y, button, modifiers):
        """Use a mouse press to advance to the 'game' view."""
        MainMenuMech(x, y, self.window)
        game_over = GameOverView(winner(self.field), self.fieldsize)
        self.window.show_view(game_over)

class GameOverView(arcade.View):

    def __init__(self, winner, fieldsize):
        super().__init__()
        self.winner = winner
        self.fieldsize = fieldsize

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        if self.winner == "o":
            text = "AI won the game, click mouse to restart"
        elif self.winner == "x":
            text = "You won the game! Click mouse to restart"
        else:
            text = "It's a draw, click mouse to restart"

        self.clear()
        arcade.draw_text(
            text,
            800 / 2,
            800 / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        MainMenuButton()

    def on_mouse_press(self, x, y, button, modifiers):
        """Use a mouse press to advance to the 'game' view."""
        MainMenuMech(x, y, self.window)
        game_view = MyGame(self.fieldsize)
        self.window.show_view(game_view)

def main():
    window = arcade.Window(800, 800, "New Tic Tac Toe Game")
    main_menu = MainMenu()
    window.show_view(main_menu)
    arcade.run()

if __name__ == "__main__":
    main()


