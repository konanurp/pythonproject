###############################################################################
#Project 10
#Game of Reversi (Othello)
#Take turns between placing black and white tiles
#Objective: Have the most tiles by the end of the game
###############################################################################
import reversi
import string
LETTERS = string.ascii_lowercase

def indexify(position):
    '''
    This function takes the alphanum position and converts it to a row,col
    '''
    #Creating dict where key=alpha, val=num
    alpha_num_dict = {}
    for_counter = 0
    for ch in string.ascii_lowercase:
        alpha_num_dict[ch] = for_counter
        for_counter += 1
        
    i_row = position[0]
    i_col = position[1:]
    i_col = int(i_col)
    
    row = alpha_num_dict[i_row]
    col = i_col - 1
    
    return row,col

def deindexify(row, col):
    '''
    This function takes a row,col and converts it to a alphanum position
    '''
    #Creating dict where key=num, val=alpha
    num_alpha_dict = {}
    alpha_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
                  'p','q','r','s','t','u','v','w','x','y','z']
    alpha_list_index = 0
    for i in range(0,26):
        num_alpha_dict[i] = alpha_list[alpha_list_index]
        alpha_list_index += 1
        
    position_a = num_alpha_dict[row]
    position_n = col + 1
    position_n = str(position_n)
    
    position = position_a + position_n
    return position
    
    
def initialize(board):
    '''
    This function places the opening four tiles for the game
    '''
    size = board.length
    size_rem = size % 2
    if size_rem == 0:
        top = int((size / 2) - 1)
        bottom = int((size / 2))
        board.place(top,top,reversi.Piece('white'))
        board.place(top,bottom,reversi.Piece('black'))
        board.place(bottom,top,reversi.Piece('black'))
        board.place(bottom,bottom,reversi.Piece('white'))
    elif size_rem == 1:
        size = size - 1
        top = int((size / 2) - 1)
        bottom = int((size / 2))
        board.place(top,top,reversi.Piece('white'))
        board.place(top,bottom,reversi.Piece('black'))
        board.place(bottom,top,reversi.Piece('black'))
        board.place(bottom,bottom,reversi.Piece('white'))    

def count_pieces(board):
    '''
    This function counts all of the white tiles and black tiles when called
    '''
    total_black = 0
    total_white = 0
    something = 3
    size = board.length
    
    for row in range(board.length):
        for col in range(board.length):
            q = board.get(row,col)
            if board.is_free(row,col) == True:
                something += 1
            elif board.is_free(row,col) == False:
                if q.is_black() == True:
                    total_black += 1
                elif q.is_white() == True:
                    total_white += 1
                    
    return total_black,total_white

def get_all_streaks(board, row, col, piece_arg):
    '''
    This function takes in board, piece, row, and col and returns a dictionary 
    with key=direction and val=possible captures
    '''
    streaks = {'e': None, 'w': None, 'n': None, 's': None, \
               'ne': None, 'nw': None, 'se': None, 'sw': None}
    
    color = piece_arg.color()
    other_color = 'white' if color == 'black' else 'black'
    # north
    L = []
    c = col
    for r in range(row-1,-1,-1):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['n'] = sorted(L)

#    # east
    L = []
    c = col
    r = row
    for c in range(col+1,board.length):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['e'] = sorted(L)
 
#    # south
    L = []
    c = col
    r = row
    for r in range(row+1,board.length):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['s'] = sorted(L)

#    # west
    L = []
    c = col
    r = row
    for c in range(col-1,-1,-1):
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
    else:
        L = [] # streak not terminated with color piece
    streaks['w'] = sorted(L)

#    # northeast
    L = []
    c = col
    r = row
    c = col+1
    for r in range(row-1,-1,-1):
        if c == board.length:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c += 1
    else:
        L = [] # streak not terminated with color piece
    streaks['ne'] = sorted(L)
        
#    # southeast
    L = []
    c = col
    r = row
    c = col+1
    for r in range(row+1,board.length):
        if c == board.length:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c += 1
    else:
        L = [] # streak not terminated with color piece
    streaks['se'] = sorted(L)
                
#    # southwest
    L = []
    c = col
    r = row
    c = col - 1
    for r in range(row+1,board.length):
        if c == -1:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c = c - 1
    else:
        L = [] # streak not terminated with color piece
    streaks['sw'] = sorted(L)
    
#    # northwest
    L = []
    c = col
    r = row
    c = col - 1
    for r in range(row-1,-1,-1):
        if c == -1:
            L = []  # terminated without finding color
            break
        if not board.is_free(r,c):
            piece = board.get(r,c)
            if piece.color() == other_color:
                L.append((r,c))
            else:
                break # terminated streak with color
        else:
            L = []  # terminated without finding color
            break
        c = c - 1
    else:
        L = [] # streak not terminated with color piece
    streaks['nw'] = sorted(L)
            
    return streaks

def get_all_capturing_cells(board, piece):
    '''
    This function creates a dictionary containing positions that can be played
    '''
    something = 5
    cap_cells_dict = {}
    for row in range(board.length):
        for col in range(board.length):
            if board.is_free(row,col) == True:
                solution = get_all_streaks(board,row,col,piece)
                a_list = []
                for val in solution.values():
                    for thing in val:
                        if val == []:
                            something += 1
                        else:
                            a_list.append(thing)
                sorted_list = sorted(a_list)
                if sorted_list == []:
                    continue
                cap_cells_dict[row,col] = sorted_list
                            
    return cap_cells_dict

def get_hint(board, piece):
    '''
    This function returns a list of best options of play when called upon
    '''
    streaks_dict = get_all_capturing_cells(board,piece)
    intermed_list = []
    for key,val in streaks_dict.items():
        b_list = []
        position = deindexify(key[0],key[1])
        length = len(val)
        b_list.append(length)
        b_list.append(position)
        intermed_list.append(b_list)
    sorted_list = sorted(intermed_list, reverse=True)
    positions_list = []
    for item in sorted_list:
        positions_list.append(item[1])
    return positions_list
    
def place_and_flip(board, row, col, piece):
    '''
    This function places tiles on place of choice and flips tiles
    '''
    solution = get_all_streaks(board,row,col,piece)
    chosen_position = deindexify(row,col)
    color = piece.color()
    
    list_of_poss = []
    for val in solution.values():
        if val != []:
            list_of_poss.append(val)
            
    if len(list_of_poss) == 0:
        if color == "white":
            color = "W"
        elif color == "black":
            color = "B"
        print("Error: Can't place {:s} at '{:s}', it's not a capture. Type 'hint' to get suggestions".format(color,chosen_position))
        return "nothing"
    elif not board.is_free(row,col):
        if color == "white":
            color = "W"
        elif color == "black":
            color = "B"
        print("Error: Can't place {:s} at '{:s}', already occupied. Type 'hint' to get suggestions.".format(color,chosen_position))
        return "nothing"
    
    else:
        board.place(row,col,piece)
        #Removing old pieces and putting new pieces back in
        for item in list_of_poss:
            for thing in item:
                board.remove(thing[0],thing[1])
        for item in list_of_poss:
            for thing in item:
                board.place(thing[0],thing[1],piece)

def is_game_finished(board):
    '''
    This function determines if the game can go on any further
    '''
    black_list = get_hint(board, reversi.Piece('black'))
    white_list = get_hint(board, reversi.Piece('white'))
    black_list_len = len(black_list)
    white_list_len = len(white_list)
    
    if board.is_full() == True:
        return True
    elif black_list_len == 0 and white_list_len == 0:
        return True
    else:
        return False
def get_winner(board):
    '''
    This function determines the winner by counting the number of tiles for
    each player
    '''
    total_black,total_white = count_pieces(board)
    
    if total_black > total_white:
        return "black"
    elif total_black < total_white:
        return "white"
    elif total_black == total_white:
        return "draw"
    
def choose_color():
    color_counter = 0
    while color_counter == 0:
        color_choice = input("Pick a color: ")
        color_choice = color_choice.lower()
        if color_choice == "black":
            my_color = color_choice
            opponent_color = "white"
            print("You are '{:s}' and your opponent is '{:s}'.".format(my_color,opponent_color))
            return my_color, opponent_color
        elif color_choice == "white":
            my_color = color_choice
            opponent_color = "black"
            print("You are '{:s}' and your opponent is '{:s}'.".format(my_color,opponent_color))
            return my_color, opponent_color
        else:
            print("Wrong color, type only 'black' or 'white', try again.")

def game_play_human():
    """
    This is the main mechanism of the human vs. human game play.
    """
    
    banner = """
     _____                         _ 
    |  __ \                       (_)
    | |__) |_____   _____ _ __ ___ _ 
    |  _  // _ \ \ / / _ \ '__/ __| |
    | | \ \  __/\ V /  __/ |  \__ \ |
    |_|  \_\___| \_/ \___|_|  |___/_|
    
    Developed by The Students Inc.
    CSE231 Spring Semester 2018
    Michigan State University
    East Lansing, MI 48824, USA.
    """

    prompt = "[{:s}'s turn] :> "
    print(banner)
   
    # Choose the color here
    (my_color, opponent_color) = choose_color()
    
    # Take a board of size 8x8
    # Prompt for board size
    size = input("Input a board size: ")
    board = reversi.Board(int(size))
    initialize(board)
    
    # Decide on whose turn, use a variable called 'turn'.
    turn = my_color if my_color == 'white' else opponent_color
    
    # loop until the game is finished
    while not is_game_finished(board):
        try:
            # Count the pieces and assign into piece_count
            piece_count = count_pieces(board)
            
            print("Current board:")
            board.display(piece_count)    
            
            # Get a piece according to turn
            piece = reversi.Piece(turn)
            
            # Get the command from user using input
            command = input(prompt.format(turn)).lower()
            
            # Now decide on different commands
            if command == 'exit':
                break
            elif command == 'hint':
                print("\tHint: " + ", ".join(get_hint(board, piece)))
            elif command == 'pass':
                hint = get_hint(board, piece)
                if len(hint) == 0:
                    turn = my_color if turn == opponent_color \
                                        else opponent_color
                    print("\tHanded over to \'{:s}\'.".format(turn))
                else:
                    print("\tCan't hand over to opponent, you have moves," + \
                          " type \'hint\'.")
            else:
                    (row, col) = indexify(command)
                    solution = place_and_flip(board, row, col, piece)
                    if solution == "nothing":
                        continue
                    print("\t{:s} played {:s}.".format(turn, command))
                    turn = my_color if turn == opponent_color \
                                        else opponent_color
        except Exception as err:
            print("Error:", err)
    
    # The loop is over.
    piece_count = count_pieces(board)
    print("Current board:")
    board.display(piece_count)    
    winner = get_winner(board)
    if winner != 'draw':
        diff = abs(piece_count[0] - piece_count[1])
        print("\'{:s}\' wins by {:d}! yay!!".format(winner, diff))
    else:
        print("This game ends in a draw.")
    # --- end of game play ---
    
def figure_1(board):
    """
    You can use this function to test your program
    """
    board.place(0,0,reversi.Piece('black'))
    board.place(0,3,reversi.Piece('black'))
    board.place(0,4,reversi.Piece('white'))
    board.place(0,5,reversi.Piece('white'))
    board.place(0,6,reversi.Piece('white'))
    board.place(1,1,reversi.Piece('white'))
    board.place(1,3,reversi.Piece('white'))
    board.place(1,5,reversi.Piece('white'))
    board.place(1,6,reversi.Piece('white'))
    board.place(1,7,reversi.Piece('white'))
    board.place(2,2,reversi.Piece('white'))
    board.place(2,3,reversi.Piece('black'))
    board.place(2,4,reversi.Piece('white'))
    board.place(2,5,reversi.Piece('white'))
    board.place(2,7,reversi.Piece('white'))
    board.place(3,0,reversi.Piece('black'))
    board.place(3,1,reversi.Piece('white'))
    board.place(3,2,reversi.Piece('white'))
    board.place(3,4,reversi.Piece('white'))
    board.place(3,5,reversi.Piece('white'))
    board.place(3,6,reversi.Piece('black'))
    board.place(3,7,reversi.Piece('black'))
    board.place(4,0,reversi.Piece('white'))
    board.place(4,2,reversi.Piece('white'))
    board.place(4,4,reversi.Piece('white'))
    board.place(5,0,reversi.Piece('black'))
    board.place(5,2,reversi.Piece('black'))
    board.place(5,3,reversi.Piece('white'))
    board.place(5,5,reversi.Piece('black'))
    board.place(6,0,reversi.Piece('black'))
    board.place(6,1,reversi.Piece('black'))
    board.place(6,3,reversi.Piece('white'))
    board.place(6,6,reversi.Piece('white'))
    board.place(7,1,reversi.Piece('black'))
    board.place(7,2,reversi.Piece('white'))
    board.place(7,3,reversi.Piece('black'))
    board.place(7,7,reversi.Piece('black'))
    
if __name__ == "__main__":
    game_play_human()