import pygame
import os

#to map the file name
piece_name_mapping = {
    'p': 'pawn',
    'r': 'rook',
    'n': 'knight',
    'b': 'bishop',
    'q': 'queen',
    'k': 'king',
}

#initializing the chessboard with pieces in their initial positions.
def initialize_board():
    board_state = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    return board_state

#loading images into the chessboard, and scaling 'em.
def load_and_scale_image(path, new_size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, new_size)

#setting up the board
def draw_board(screen, square_size, board_color_1, board_color_2, king_in_check):
    #drawing the static chessboard squares
    for row in range(8):
        for col in range(8):
            color = board_color_1 if (row + col) % 2 == 0 else board_color_2
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))
    
    #if the king is in check, highlight its square
    if king_in_check is not None:
        highlight_color = (255, 0, 0)  #red color for highlighting the king's square
        pygame.draw.rect(screen, highlight_color, (king_in_check[1] * square_size, king_in_check[0] * square_size, square_size, square_size), 5)

#settin up the pieces inside the board
def draw_pieces(screen, square_size, board_state, white_pieces, black_pieces):
    for row in range(8):
        for col in range(8):
            piece_code = board_state[row][col] 
            if piece_code != ' ':
                #determining the color and get the full piece name
                color = 'white' if piece_code.isupper() else 'black'
                piece_name = piece_name_mapping[piece_code.lower()]  #Using the mapping
                
                #To Fetch the correct image based on color and piece name
                piece_img = white_pieces[piece_name] if color == 'white' else black_pieces[piece_name]
                
                #set up each of the piece
                screen.blit(piece_img, (col * square_size, row * square_size))


#returns a list of legal moves for the given piece and position.
def get_legal_moves(piece, position, board_state, player):
    row, col = position
    moves = []
    direction = -1 if player == 'white' else 1  #white pawns move up (decreasing row), black pawns move down (increasing row)
    
    #define a function to check if an opponent's piece occupies a square
    def is_opponent_piece(r, c):
        return board_state[r][c].isalpha() and ((player == 'white' and board_state[r][c].islower()) or (player == 'black' and board_state[r][c].isupper()))

    #define a function to check if a square is empty
    def is_empty_square(r, c):
        return board_state[r][c] == ' '
    
    #for the pawn
    if piece.lower() == 'p':
        #move forward
        if is_empty_square(row + direction, col):
            moves.append((row + direction, col))
            #starting move: 2 squares
            if (player == 'white' and row == 6) or (player == 'black' and row == 1):
                if is_empty_square(row + 2 * direction, col):
                    moves.append((row + 2 * direction, col))
        #Captures diagonally
        for dcol in [-1, 1]:
            capture_col = col + dcol
            capture_row = row + direction
            if 0 <= capture_col < 8 and 0 <= capture_row < 8 and is_opponent_piece(capture_row, capture_col):
                moves.append((capture_row, capture_col))
                
    # for the Knight
    if piece.lower() == 'n':
        # for the "L" shape movement
        move_offsets = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)] 
        for dr, dc in move_offsets:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if is_empty_square(new_row, new_col) or is_opponent_piece(new_row, new_col):
                    moves.append((new_row, new_col))
                    
    #for the bishop
    if piece.lower() == 'b':
        #Diagonal movements
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if is_empty_square(r, c):
                    moves.append((r, c))
                elif is_opponent_piece(r, c):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    # for the rook
    if piece.lower() == 'r':
        #hrizontal and vertical movements
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if is_empty_square(r, c):
                    moves.append((r, c))
                elif is_opponent_piece(r, c):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    #for the Queen
    if piece.lower() == 'q':
        #horizontal, vertical, and diagonal movements
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if is_empty_square(r, c):
                    moves.append((r, c))
                elif is_opponent_piece(r, c):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

    #for the King
    if piece.lower() == 'k':
        #surrounding squares
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    if is_empty_square(r, c) or is_opponent_piece(r, c):
                        moves.append((r, c))

    #to filter out moves that would capture the player's own piece
    moves = [move for move in moves if not (0 <= move[0] < 8 and 0 <= move[1] < 8 and board_state[move[0]][move[1]] != ' ' and ((player == 'white' and board_state[move[0]][move[1]].isupper()) or (player == 'black' and board_state[move[0]][move[1]].islower())))]

    return moves

#highlights legal moves on the board.  
def highlight_moves(screen, square_size, legal_moves):
    highlight_color = (0, 120, 100) #highlight color
    for move in legal_moves:
        row, col = move
        #draw a filled circle in the center of the square to indicate a legal move
        center_position = (col * square_size + square_size // 2, row * square_size + square_size // 2)
        pygame.draw.circle(screen, highlight_color, center_position, square_size // 5) #the size of the circle can be adjusted by changing square_size // x, put higher x for smaller circle.

#moves a piece from start_pos to end_pos in board_state.
def move_piece(start_pos, end_pos, board_state):
    piece = board_state[start_pos[0]][start_pos[1]]
    board_state[start_pos[0]][start_pos[1]] = ' '  #empty the start position
    board_state[end_pos[0]][end_pos[1]] = piece  #place the piece at the end position
    return board_state  #ensure you return the updated board_state

#returns 'white' or 'black' based on the move count.
def get_current_player(move_count):
    return 'white' if move_count % 2 == 0 else 'black'

#loop through the entire board to look for opponent's pieces and see if they can capture the king    
def is_in_check(king_pos, board_state, opponent):
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if piece != ' ' and ((opponent == 'white' and piece.isupper()) or (opponent == 'black' and piece.islower())):
                if king_pos in get_legal_moves(piece, (row, col), board_state, opponent):
                    return True
    return False

#check if the player's king is in check
def is_checkmate(king_pos, board_state, player):
    if not is_in_check(king_pos, board_state, 'black' if player == 'white' else 'white'):
        return False  #if king is not in check, so it can't be checkmate :D

    #check for any legal moves that would remove the check
    for row in range(8):
        for col in range(8):
            piece = board_state[row][col]
            if (player == 'white' and piece.isupper()) or (player == 'black' and piece.islower()):
                legal_moves = get_legal_moves(piece, (row, col), board_state, player)
                for move in legal_moves:
                    simulated_board_state = simulate_move(board_state, (row, col), move)
                    if not is_in_check(find_king(simulated_board_state, player), simulated_board_state, 'black' if player == 'white' else 'white'):
                        return False  #found a legal move that removes the check
    return True #no legal moves remove the check, it's checkmate

#to get the location of the king
def find_king(board_state, player):
    king = 'K' if player == 'white' else 'k'
    for row in range(8):
        for col in range(8):
            if board_state[row][col] == king:
                return row, col

#simulates a move on a copy of the board state and returns the new board state.
def simulate_move(board_state, start_pos, end_pos):
    """:param board_state: Current board state.
    :param start_pos: The starting position of the piece (row, col).
    :param end_pos: The ending position of the piece (row, col).
    :return: A new board state after the move.
    """
    #create a deep copy of the board to not affect the original board
    new_board_state = [row[:] for row in board_state]

    start_row, start_col = start_pos
    end_row, end_col = end_pos

    #move the piece
    piece = board_state[start_row][start_col]
    new_board_state[start_row][start_col] = ' '  #remove the piece from the start position
    new_board_state[end_row][end_col] = piece  #place the piece at the end position

    return new_board_state

#to filter moves if the next move would be check
def filter_legal_moves_for_check(board_state, selected_piece_pos, legal_moves, player):
    filtered_moves = []
    for move in legal_moves:
        #simulate the move, ie, make the code 'imagine' if this move was played would it be legal.
        simulated_board_state = simulate_move(board_state, selected_piece_pos, move)
        if not is_in_check(find_king(simulated_board_state, player), simulated_board_state, 'black' if player == 'white' else 'white'):
            filtered_moves.append(move)
    return filtered_moves

