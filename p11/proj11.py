################################################################################
# Computer Project 11
#
# This program allows two people to play eachother in the game of Gomoku.
#
# 1 Get intial parameters
# 2 Loop until quit or win
# 3   prompt for position to place Go stone at
# 4   if input is ok, then put player's Go stone at position
# 5   else goto 3
# 6   if player has won, print winner's color and exit
# 7   switch current player
################################################################################
class GoPiece(object):
    ''' Represents a Go piece. Usually is a small black or white stone. Fun to
    put on a Go board. '''

    def __init__(self, color='black'):
        ''' Make a Go piece that has a color of either 'black' or 'white'.
        Raises an exception if color is not black or white.'''
        color = color.lower()
        if color not in ['black', 'white']:
            raise MyError('Wrong color.')
        self.__color = color

    def __str__(self):
        ''' Converts the Go piece into a fancy string. '''
        if self.__color == 'black':
            return ' ● '
        else:
            return ' ○ '

    def get_color(self):
        ''' Return the color the Go piece was initialized with. '''
        return self.__color

class MyError(Exception):
    def __init__(self,value):
        self.__value = value
    def __str__(self):
        return self.__value

class Gomoku(object):
    ''' Manages the board, pieces, and current player of the game Gomoku. '''

    def __init__(self,board_size=15,win_count=5,current_player='black'):
        ''' Initialized a game of Gomoku, possibly with specific parameters.
        Raises appropriate exceptions if the parameters are not in the correct
        range or are the correct type.
        board_size: size of the square board that Gomoku is played on (int)
        win_count: minimum number of pieces in an unbroken line to win (int)
        current_player: the initial player ('black' or 'white')
        Tic-Tac-Toe with board_size==win_count==3.'''
        if type(board_size) != int:
            raise ValueError
        if type(win_count) != int:
            raise ValueError
        if current_player not in ['black', 'white']:
            raise MyError('Wrong color.')

        if not (win_count > 0):
            raise MyError('Wrong win_count.')
        if not (board_size > 0):
            raise MyError('Wrong board_size.')
        if win_count > board_size:
            raise MyError('win_count must be less than board_size.')

        self.__board_size = board_size
        self.__win_count = win_count
        self.__current_player = current_player
        # 2D square array
        self.__go_board = [[' - ']*board_size for j in range(board_size)]

    def assign_piece(self,piece,row,col):
        ''' Try to place the Go piece on the board at (row, col)
        Raise an exception if row or col are not on the board,
        or if the board at (row, col) already contains a Go piece. '''
        # convert to zero based indices
        row -= 1
        col -= 1

        if not (0 <= row < self.__board_size):
            raise MyError('Invalid position.')
        if not (0 <= col < self.__board_size):
            raise MyError('Invalid position.')
        if self.__go_board[row][col] != ' - ':
            raise MyError('Position is occupied.')

        self.__go_board[row][col] = piece

    def get_current_player(self):
        ''' Returns the current player as a string, 'black' or 'white' '''
        return self.__current_player

    def switch_current_player(self):
        ''' Switch to the player for the next turn. '''
        if self.__current_player == 'black':
            self.__current_player = 'white'
        else:
            self.__current_player = 'black'
        return self.__current_player

    def __str__(self):
        s = '\n'
        for i,row in enumerate(self.__go_board):
            s += "{:>3d}|".format(i+1)
            for item in row:
                s += str(item)
            s += "\n"
        line = "___"*self.__board_size
        s += "    " + line + "\n"
        s += "    "
        for i in range(1,self.__board_size+1):
            s += "{:>3d}".format(i)
        s += "\n"
        s+='Current player: '+('●' if self.__current_player == 'black' else '○')
        return s

    def current_player_is_winner(self):
        ''' Return if the current player has won the game. This function checks
        if the current player has placed an unbroken sequence of
        self.__win_count number of Go stones onto the board in a straight line
        (horizontally, vertically or diagonally). '''


        # iff the win_str is in a row string, will the current player win.
        win_str = self.__win_count * str(GoPiece(self.__current_player))
        # S(x) will convert a row, col, or diag list into a string
        def S(x):
            return ''.join(map(str, x))

        # Check horizontals
        board = self.__go_board
        for row in board:
            if win_str in S(row):
                return True
        # Transpose board
        board = list(zip(*board))
        # Check verticals
        for col in board:
            if win_str in S(col):
                return True
        # Check diagonals
        bsz = self.__board_size
        # There are no diagonal wins if len(diagonal) < self.__win_count
        for i in range(bsz - (self.__win_count - 1)):
            # The diagonal that is i units, horizontally, away from the main
            # diagonal has length bsz-i
            r = range(bsz-i)

            # diagonal in lower left triangle of board
            if win_str in S([board[i+j][j] for j in r]):
                return True

            # diagonal in upper right triangle of board
            if win_str in S([board[j][i+j] for j in r]):
                return True

            # diagonal in  lower right triangle of board
            if win_str in S([board[i+j][bsz-1-j] for j in r]):
                return True

            # diagonal in  upper left triangle of board
            if win_str in S([board[j][bsz-1-(i+j)] for j in r]):
                return True
        return False

        ########################### O(bsz**3) ? ########### Other implementation
        #board = [ [ str(p) for p in row ] for row in self.__go_board ]
        #bsz = self.__board_size
        #for row in range(bsz):
        #    for col in range(bsz):
        #        h_prev = None
        #        v_prev = None
        #        d_prev = None
        #        h_sum = 0
        #        v_sum = 0
        #        d_sum = 0
        #        for p in range(bsz):
        #            r = row + p
        #            c = col + p
        #            if r < bsz and c < bsz:
        #                gp = board[r][c]
        #                if gp != ' - ':
        #                    if gp == d_prev:
        #                        d_sum += 1
        #                    else:
        #                        d_prev = gp
        #                        d_sum = 1
        #                else:
        #                    d_sum = 0
        #                    d_prev = None
        #            if r < bsz:
        #                gp = board[r][col]
        #                if gp != ' - ':
        #                    if gp == v_prev:
        #                        v_sum += 1
        #                    else:
        #                        v_prev = gp
        #                        v_sum = 1
        #                else:
        #                    v_sum = 0
        #                    v_prev = None
        #            if c < bsz:
        #                gp = board[row][c]
        #                if gp != ' - ':
        #                    if gp == h_prev:
        #                        h_sum += 1
        #                    else:
        #                        h_prev = gp
        #                        h_sum = 1
        #                else:
        #                    h_sum = 0
        #                    h_prev = None
        #            if v_sum >= self.__win_count or h_sum >= self.__win_count \
        #                or d_sum >= self.__win_count:
        #                    return True
        #return False

        ########################### O(bsz**2) ? ########### Other implementation
        #board = [ [ str(p) for p in row ] for row in self.__go_board ]
        #bsz = self.__board_size
        #wc = self.__win_count
        #h_sum = 0
        #v_sum = 0
        #d1_sum = 0
        #d2_sum = 0
        #d3_sum = 0
        #d4_sum = 0
        #h_prv = None
        #v_prv = None
        #d1_prv = None
        #d2_prv = None
        #d3_prv = None
        #d4_prv = None
        #for i in range(bsz**2):

        #    row = i // bsz
        #    col = i % bsz

        #    if col == 0:
        #        h_sum = 0
        #        h_prv = None
        #        v_sum = 0
        #        v_prv = None

        #    gp = board[row][col]
        #    if gp != ' - ':
        #        if gp == h_prv:
        #            h_sum += 1
        #        else:
        #            h_sum = 1
        #            h_prv = gp
        #    else:
        #        h_prv = None

        #    gp = board[col][row]
        #    if gp != ' - ':
        #        if gp == v_prv:
        #            v_sum += 1
        #        else:
        #            v_sum = 1
        #            v_prv = gp
        #    else:
        #        v_prv = None

        #    if row + col >= bsz:
        #        d1_sum = 0
        #        d2_sum = 0
        #        d3_sum = 0
        #        d4_sum = 0
        #        d1_prv = None
        #        d2_prv = None
        #        d3_prv = None
        #        d4_prv = None

        #    if row + col < bsz:
        #        gp = board[row+col][col]
        #        if gp != ' - ':
        #            if gp == d1_prv:
        #                d1_sum += 1
        #            else:
        #                d1_sum = 1
        #                d1_prv = gp
        #        else:
        #            d1_prv = None
        #        gp = board[col][row+col]
        #        if gp != ' - ':
        #            if gp == d2_prv:
        #                d2_sum += 1
        #            else:
        #                d2_sum = 1
        #                d2_prv = gp
        #        else:
        #            d2_prv = None
        #        gp = board[row+col][bsz-1-col]
        #        if gp != ' - ':
        #            if gp == d3_prv:
        #                d3_sum += 1
        #            else:
        #                d3_sum = 1
        #                d3_prv = gp
        #        else:
        #            d3_prv = None
        #        gp = board[col][bsz-1-(row+col)]
        #        if gp != ' - ':
        #            if gp == d4_prv:
        #                d4_sum += 1
        #            else:
        #                d4_sum = 1
        #                d4_prv = gp
        #        else:
        #            d4_prv = None
        #    if wc <= max([h_sum, v_sum, d1_sum, d2_sum, d3_sum, d4_sum]):
        #        return True
        #return False


def main():
    G = Gomoku()
    print(G)
    play = input("Input a row then column separated by a comma (q to quit): ")
    # Play the game until a player quits or wins the game.
    while play.lower() != 'q':
        did_except = False # reprompt player if invalid input
        try:
            # Get valid inputs
            try:
                play_list = play.strip().split(',')
                row = int(play_list[0])
                col = int(play_list[1])
            except:
                raise MyError("Incorrect input.")

            G.assign_piece(GoPiece(G.get_current_player()), row, col)
        except MyError as error_message:
            print("{:s}\nTry again.".format(str(error_message)))
            did_except = True
        if not did_except:
            if G.current_player_is_winner():
                print(G)
                print("{} Wins!".format(G.get_current_player()))
                break
            G.switch_current_player()
        print(G)
        play=input("Input a row then column separated by a comma (q to quit): ")

if __name__ == '__main__':
    main()
