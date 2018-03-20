################################################################################
#
# Computer Project 10
#
# This game allows two players to play the game nine men's morris.
#
###### GAME RULES
# -The game has two phases and in each phase players take turns placing tokens
# on the game board.
#
# -The game board is made up of 8*3 = 24 positions where each position can
# contain one player's token or no token and certain positions are connected
# to other positions via edges.
#
# -The board is laid out like this,   *--------*--------*
# * = positions                       |        |        |
# - = edge                            |  *-----*-----*  |
# | = edge                            |  |     |     |  |
#                                     |  |  *--*--*  |  |
#                                     |  |  |     |  |  |
#                                     *--*--*     *--*--*
#                                     |  |  |     |  |  |
#                                     |  |  *--*--*  |  |
#                                     |  |     |     |  |
#                                     |  *-----*-----*  |
#                                     |        |        |
#                                     *--------*--------*
#
# -If a player puts a token on a position, then the player owns that position.
# -If the player owns three positions that are in a straight line and are
# connected by edges, then the positions are in a mill.
#
# -In the first phase the two players take turns placing their tokens on the
# board. If a mill is formed by a player, then the player immediately removes
# one of the other player's tokens that is not in a mill. If all the other
# player's tokens are in a mill, then the player can remove any token.
#
# -After each player has had 9 turns, the game moves into the second phase.
#
# -In the second phase the two players take turns moving their tokens around the
# board. Again, if a mill is formed by a player, then the player immediately
# removes one of the other player's tokens that is not in a mill. If all the
# other player's tokens are in a mill, then the player can remove any token.
#
# -A player wins in the second phase at the end of a turn if the opposite player
# has less than three tokens on the board.
#
###### CODE DETAILS
# The board is a dictionary that maps each point (position) to a token string
# or an empty space (the point isn't taken yet).
# The player is represented as their token strings, either 'X' or 'O'.
#
# Control Flow
# loop until restart or quit
#     phase1
#         loop until loop_counter == 18 (18 turns taken), or until quit/restart
#             get player's input
#             if user gives valid input
#                 place peice
#                 if formed mill
#                     prompt for piece to remove, until user gives valid input
#                     remove piece
#                 increment loop_counter every time player's turn ends
#             else
#                 try again
#     phase2
#         loop until game over, quit, or restart
#             get player's input
#             if user gives valid input
#                 move piece
#                 if formed mill
#                     prompt for piece to remove, until user gives valid input
#                     remove piece
#                 if player has won, then print congrats and exit
#
################################################################################

from NMM import Board

WIN_BANNER = """
    __        _____ _   _ _   _ _____ ____  _ _ _ 
    \ \      / /_ _| \ | | \ | | ____|  _ \| | | |
     \ \ /\ / / | ||  \| |  \| |  _| | |_) | | | |
      \ V  V /  | || |\  | |\  | |___|  _ <|_|_|_|
       \_/\_/  |___|_| \_|_| \_|_____|_| \_(_|_|_)

"""


RULES = """
  _   _ _              __  __            _       __  __                 _     
 | \ | (_)_ __   ___  |  \/  | ___ _ __ ( )___  |  \/  | ___  _ __ _ __(_)___ 
 |  \| | | '_ \ / _ \ | |\/| |/ _ \ '_ \|// __| | |\/| |/ _ \| '__| '__| / __|
 | |\  | | | | |  __/ | |  | |  __/ | | | \__ \ | |  | | (_) | |  | |  | \__ \
 |_| \_|_|_| |_|\___| |_|  |_|\___|_| |_| |___/ |_|  |_|\___/|_|  |_|  |_|___/
                                                                                        
    The game is played on a grid where each intersection is a "point" and
    three points in a row is called a "mill". Each player has 9 pieces and
    in Phase 1 the players take turns placing their pieces on the board to 
    make mills. When a mill (or mills) is made one opponent's piece can be 
    removed from play. In Phase 2 play continues by moving pieces to 
    adjacent points. 
    
    The game is ends when a player (the loser) has less than three 
    pieces on the board.

"""

HELP = """

    Game commands (first character is a letter, second is a digit):
    
    xx        Place piece at point xx (only valid during Phase 1 of game)
    xx yy     Move piece from point xx to point yy (only valid during Phase 2)
    R         Restart the game
    H         Display this menu of commands
    Q         Quit the game
    
"""

def player_owns_all(board, positions, player):
    """
    Return true if player has a token at all three places in positions.
    board: a Board instance
    positions: a list of three token strings
    player: player's token string
    """
    return board.points[positions[0]] == player\
       and board.points[positions[1]] == player\
       and board.points[positions[2]] == player

def count_mills(board, player):
    """
    Return the count of mills on the board that are owned by player.
    board: a Board instance
    player: player's token string
    """
    mill_count = 0
    for mill in Board.MILLS:
        if player_owns_all(board, mill, player):
            mill_count += 1
    return mill_count

def place_piece_and_remove_opponents(board, player, destination):
    """
    Place player's token on the board at destination.
    Will raise a runtime error if player or destination inputs are incorrect.
    If a mill is formed then the player is prompted to remove one of the
    opponent's tokens.
    board: a Board instance
    player: player's token string
    """

    # Can token be placed?
    if board.points[destination] in [player, get_other_player(player)]:
        raise RuntimeError("Invalid command: Destination point already taken")
    if destination not in board.points:
        raise RuntimeError("Invalid command: Not a valid point")

    # Token can be placed

    # If count increases, then a token was successfully placed
    mill_count = count_mills(board, player)
    board.assign_piece(player, destination)
    mill_created = mill_count < count_mills(board, player)
    if mill_created:
        print("A mill was formed!")
        print(board)
        remove_piece(board, get_other_player(player))

def move_piece(board, player, origin, destination):
    """
    Moves a player's token from origin to destination if possible.
    The function will raise an error if player, origin or destination is
    invalid.
    board: a Board instance
    player: player's token string
    origin: a board position string
    destination: a board position string
    """

    # Can token can be moved?
    if destination not in board.points:
        raise RuntimeError("Invalid command: Not a valid point")
    if origin not in board.points:
        raise RuntimeError("Invalid command: Not a valid point")
    if destination not in Board.ADJACENCY[origin]:
        raise RuntimeError("Invalid command: Destination is not adjacent")
    my_points = placed(board, player)
    if origin not in my_points:
        err_str = "Invalid command: Origin point does not belong to player"
        raise RuntimeError(err_str)
    if board.points[destination] != ' ':
        raise RuntimeError("Invalid command: Destination point already taken")

    # Token can be moved.
    board.clear_place(origin)
    place_piece_and_remove_opponents(board, player, destination)

def points_not_in_mills(board, player) -> set:
    """
    Returns the set of points that belong to player and are not in a mill.
    Returns: a set instance
    board: a Board instance
    player: player's token string
    """
    my_points = placed(board, player)
    # For each point that is in a mill, remove that point from my set of points
    for points in Board.MILLS:
        if player_owns_all(board, points, player):
            for point in points:
                my_points.discard(point)
    return my_points

def placed(board, player) -> set:
    """ Returns the set of points on the board that are owned by player. """
    return {x for x, v in board.points.items() if v == player}

def remove_piece(board, player):
    """
    Prompts the user for a token of player to remove from the board.

    A token at position is removed given that the following conditions are met.
    1) the position is a valid board position.
    2) token belongs to player.
    3) If the token is not in a mill (unless all player's tokens are in a mill)
    Raises an error if any of the above conditions are not met.

    Repeatedly prompts the user until the user provides valid input.
    """
    my_points = placed(board, player)
    my_points_not_in_mills = points_not_in_mills(board, player)

    can_remove_from_mill = False
    if len(my_points_not_in_mills) == 0:
        can_remove_from_mill = True

    user_entered_valid_input = False
    while not user_entered_valid_input:
        try:
            point = input('Remove a piece at :> ').strip().lower()
            if point not in board.points:
                raise RuntimeError("Invalid command: Not a valid point")
            if point not in my_points:
                err_msg = "Invalid command: Point does not belong to player"
                raise RuntimeError(err_msg)
            if not can_remove_from_mill:
                if point not in my_points_not_in_mills:
                    raise RuntimeError("Invalid command: Point is in a mill")
            board.clear_place(point)
            user_entered_valid_input = True
        except RuntimeError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))

def is_winner(board, player):
    """
    Returns True if player has won, that is if we are in phase 2 and the other
    player has less than 3 tokens on the board. Otherwise returns False.
    """
    other_players_points = placed(board, get_other_player(player))
    return len(other_players_points) < 3

def get_other_player(player):
    """ Get the token string of other player. """
    return "X" if player == "O" else "O"

def phase1(board):
    """ Play phase 1 of the game.
    Returns whose turn it is, what command was most recently entered by the
    user (for quit/restart check), and the board state.
    """
    player = 'X'
    print(player + "'s turn!")
    command = input("Place a piece at :> ").strip().lower()
    print()

    # total of pieces placed by "X" or "O", includes pieces placed and then
    # removed by opponent
    placed_count = 0

    # Until someone quits, restarts, or we place all 18 pieces...
    while (command not in ['q', 'r']) and placed_count != 18:
        if command == 'h':
            print(HELP)
        else:
            # If we except, then same player is prompted again.
            did_except = False
            try:
                destination = command
                place_piece_and_remove_opponents(board, player, destination)
                placed_count += 1
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
                did_except = True
            print(board)
            if not did_except:
                player = get_other_player(player)
            print(player + "'s turn!")

        if placed_count != 18:
            command = input("Place a piece at :> ").strip().lower()
            print()

    return board, command, player

def phase2(board, player):
    """ Play phase 2 of the game.
    Returns what command was most recently entered by the user
    (for quit/restart check).
    """

    print("**** Begin Phase 2: Move pieces by specifying two points")
    command = input("Move a piece (source,destination) :> ").strip().lower()
    print()

    while command not in ['q', 'r']:
        if command == 'h':
            print(HELP)
        else:
            # If we except, then same player is prompted again.
            did_except = False
            try:
                points = command.split()
                if len(points) != 2:
                    raise RuntimeError('Invalid number of points')
                origin, destination = points
                move_piece(board, player, origin, destination)
                if is_winner(board, player):
                    print(WIN_BANNER)
                    command = 'q'
                    return command
            except RuntimeError as error_message:
                print("{:s}\nTry again.".format(str(error_message)))
                did_except = True
            print(board)
            if not did_except:
                player = get_other_player(player)
            print(player + "'s turn!")

        command = input("Move a piece (source,destination) :> ").strip().lower()
        print()

    return command

def main():
    # Loop so that we can start over on reset
    while True:
        # Setup stuff.
        board = Board()
        print(RULES)
        print(HELP)
        print(board)

        board, prev_command, player = phase1(board)

        if prev_command == 'r': # if reset
            continue
        elif prev_command == 'q': # if quit
            return

        prev_command = phase2(board, player)

        if prev_command == 'r': # if reset
            continue
        elif prev_command == 'q': # if quit
            return

if __name__ == "__main__":
    main()

###### MATH just for fun
# If we assign the nth position (counted from 0) a pair of indices i and j
# with i_n = n//8 and j_n = n%8,
# then there is an edge between two different positions x and y
#   if (i_x == i_y) and (abs(x-y) == 1 or abs(x-y) == 7)
# or
#   if (abs(i_x-i_y) == 1) and (j_x == j_y) and (j_x % 2 == 1)
#
# Three positions x1, x2, and x3, owned by one of the players, are in a mill
# if Sum(xn%2) == 1 and
#    (i_x1 == i_x2 == i_x3) and
#    (max(j_xn)-2 == min(j_xn) or (max(j_xn)+min(j_xn)==7 and Sum(j_xn) == 6+7)
# or
# if (j_x1%2 == 1) and
#    (i_x1 != i_x2 != i_x3) and
#    (j_x1 == j_x2 == j_x3)
#
# Is it always possible for one of the players to win?
# Is it every possible that we have a board conf where no player can form a mill
# in phase2
#
# CREATE ADJACENCY AND MILLS
#def pos_for_index(x):
#    i_x = x // 8
#    j_x = x % 8
#    if j_x in [0, 7, 6]:
#        x = 0
#    if j_x in [1, 5]:
#        x = 1
#    if j_x in [2, 3, 4]:
#        x = 2
#    if j_x in [0, 1, 2]:
#        y = 2
#    if j_x in [7, 3]:
#        y = 1
#    if j_x in [4, 5, 6]:
#        y = 0
#    x = 'abcdefg'[i_x:7-i_x:3-i_x][x]
#    y = '1234567'[i_x:7-i_x:3-i_x][y]
#    return x+y
#
#N = 8*3
#adjacency = [[0]*N for n in range(N)]
#for x in range(N):
#    i_x = x // 8
#    j_x = x % 8
#    for y in range(N):
#        if y == x:
#            continue
#        i_y = y // 8
#        j_y = y % 8
#        if (i_x == i_y) and (abs(x-y) == 1 or abs(x-y) == 7):
#            adjacency[x][y] = 1
#            adjacency[y][x] = 1
#        if (abs(i_x - i_y) == 1) and (j_x == j_y) and (j_x % 2 == 1):
#            adjacency[x][y] = 1
#            adjacency[y][x] = 1
#
#ADJACENCY = dict()
#for x in range(N):
#    for y in range(N):
#        if adjacency[x][y]:
#            try:
#                ADJACENCY[pos_for_index(x)].append(pos_for_index(y))
#            except:
#                ADJACENCY[pos_for_index(x)] = [pos_for_index(y)]
#
#def is_mill(x1, x2, x3):
#    is_possible_mill = False
#    i_x1 = x1//8
#    i_x2 = x2//8
#    i_x3 = x3//8
#    j_x1 = x1%8
#    j_x2 = x2%8
#    j_x3 = x3%8
#    if (i_x1 == i_x2 == i_x3):
#        parity_sum = sum([xn % 2 for xn in [x1, x2, x3]])
#        if parity_sum == 1:
#            j_xn = [j_x1, j_x2, j_x3]
#            if (max(j_xn) - 2 == min(j_xn)):
#                is_possible_mill = True
#            if (max(j_xn) + min(j_xn) == 7) and (sum(j_xn) == 6+7):
#                is_possible_mill = True
#    if (j_x1 % 2 == 1) and (i_x1 != i_x2 != i_x3) and (j_x1 == j_x2 == j_x3):
#        is_possible_mill = True
#    return is_possible_mill
#
#mills = set()
#for x1 in range(N):
#    # this should be simplified, need permutations
#    row = adjacency[x1]
#    points = []
#    if sum(row) == 2:
#        x2 = row.index(1)
#        x3 = row.index(1, x2+1)
#        if is_mill(x1, x2, x3):
#            points.append([x1, x2, x3])
#    elif sum(row) == 3:
#        x2 = row.index(1)
#        x3 = row.index(1, x2+1)
#        x4 = row.index(1, x3+1)
#        if is_mill(x1, x2, x3):
#            points.append([x1, x2, x3])
#        if is_mill(x1, x3, x4):
#            points.append([x1, x3, x4])
#        if is_mill(x1, x2, x4):
#            points.append([x1, x2, x4])
#    elif sum(row) == 4:
#        x2 = row.index(1)
#        x3 = row.index(1, x2+1)
#        x4 = row.index(1, x3+1)
#        x5 = row.index(1, x4+1)
#        if is_mill(x1, x2, x3):
#            points.append([x1, x2, x3])
#        if is_mill(x1, x3, x4):
#            points.append([x1, x3, x4])
#        if is_mill(x1, x2, x4):
#            points.append([x1, x2, x4])
#        if is_mill(x1, x3, x5):
#            points.append([x1, x3, x5])
#        if is_mill(x1, x2, x5):
#            points.append([x1, x2, x5])
#        if is_mill(x1, x4, x5):
#            points.append([x1, x4, x5])
#
#    for i in range(len(points)):
#        points[i].sort()
#        mills.add(tuple(points[i]))
#
#MILLS = []
#for points in mills:
#    lis = list(map(pos_for_index, points))
#    lis.sort()
#    MILLS.append(lis)
#MILLS.sort()
#
#import NMM
#is_eq = True
#for k,v in ADJACENCY.items():
#    if k in NMM.Board.ADJACENCY:
#        if sorted(v) != sorted(NMM.Board.ADJACENCY[k]):
#            is_eq = False
#    else:
#        is_eq = False
#    if not is_eq:
#        break
#
#print('ADJACENCY ok:')
#print(is_eq)
#is_eq = sorted(NMM.Board.MILLS) == MILLS
#print('MILLS ok:')
#print(is_eq)
################################################################################