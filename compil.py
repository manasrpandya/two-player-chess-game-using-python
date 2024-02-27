''' All the logic of the game is stored in the file 'functions.py'.
 The images needed for the game are in the pieces images folder, 
 with two subfolders Black and White, containing the necessary images.
                hope you enjoy playing :D                          '''
import pygame
import sys
from functions import *  

#initializing Pygame and set up the window
pygame.init()
window_size = (800, 800)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Chess Game - White's turn")

#defining colors anbd board settings
board_color_1 = (235, 236, 208)
board_color_2 = (119, 149, 86)
square_size = window_size[0] // 8
selected_piece_pos = None
legal_moves = []
move_count = 0
current_player = 'white'

#loading images for chess pieces
pieces = ["pawn", "knight", "bishop", "rook", "queen", "king"]
white_pieces = {}
black_pieces = {}
for fullname in piece_name_mapping.values():
    #kindly update the location of the white and black folders according to your directory!
    white_pieces[fullname] = load_and_scale_image(f'C:/Users/User/Downloads/chess/pieces images/White/{fullname}.png', (square_size, square_size))
    black_pieces[fullname] = load_and_scale_image(f'C:/Users/User/Downloads/chess/pieces images/Black/{fullname}.png', (square_size, square_size))

#initial board state setup
board_state = initialize_board()

#function to end the game
def display_end_game_message(screen, message, window_size):
    font = pygame.font.SysFont("georgia", 40)
    text_surface = font.render(message, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(window_size[0] / 2, window_size[1] / 2))

    #create a white background rectangle
    background_rect = pygame.Rect(0, 0, text_rect.width + 20, text_rect.height + 20)
    background_rect.center = text_rect.center
    pygame.draw.rect(screen, (255, 255, 255), background_rect)

    screen.blit(text_surface, text_rect)
    pygame.display.flip()
player_time = {'white': 120000, 'black': 120000}  #120000 milliseconds (2 minutes) for each player - can be adjusted according to the need.
last_tick = pygame.time.get_ticks() 
def format_time(milliseconds):
    """Convert milliseconds to minutes:seconds format."""
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

#main game loop
running = True
game_over = False
winner = None  #to keep track of the winner

while running:
    current_tick = pygame.time.get_ticks()
    dt = current_tick - last_tick
    last_tick = current_tick
    
    #update only the current player's timer to countdown
    player_time[current_player] -= dt
    
    # if current player's time runs out, end the game and declare the other player the winner
    if player_time[current_player] <= 0:
        game_over = True
        winner = 'White' if current_player == 'black' else 'Black'
        end_game_message = f"Time's up! {winner} wins by timeout!"
        display_end_game_message(screen, end_game_message, window_size)
        break  #exit the game loop immediately

    #update the window caption with the current game status and timers
    white_time_formatted = format_time(player_time['white'])
    black_time_formatted = format_time(player_time['black'])
    pygame.display.set_caption(f"Chess Game - {current_player.capitalize()}'s turn | White: {white_time_formatted} - Black: {black_time_formatted}")
    #checking for checkmate/stalemate before player makes a move
    king_pos = find_king(board_state, current_player)
    if is_checkmate(king_pos, board_state, current_player):
        pygame.display.set_caption(f"Checkmate! {'Black' if current_player == 'white' else 'White'} wins!")
        running = False
        game_over = True 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  #handling mouse click by the user
            x, y = pygame.mouse.get_pos()
            col = x // square_size
            row = y // square_size
            clicked_piece = board_state[row][col]
            if selected_piece_pos is None and clicked_piece != ' ':
                if ((current_player == 'white' and clicked_piece.isupper()) or
                    (current_player == 'black' and clicked_piece.islower())):
                    selected_piece_pos = (row, col)
                    legal_moves = get_legal_moves(clicked_piece, selected_piece_pos, board_state, current_player)               #getting legal moves
                    legal_moves = filter_legal_moves_for_check(board_state, selected_piece_pos, legal_moves, current_player)  #checking if they have moves with check
            elif selected_piece_pos:
                if (row, col) in legal_moves:
                    simulated_board_state = simulate_move(board_state, selected_piece_pos, (row, col))
                    king_pos_after_move = find_king(simulated_board_state, current_player)
                    if not is_in_check(king_pos_after_move, simulated_board_state, 'black' if current_player == 'white' else 'white'):
                        board_state = move_piece(selected_piece_pos, (row, col), board_state)
                        move_count += 1
                        current_player = 'black' if current_player == 'white' else 'white'
                        pygame.display.set_caption(f"Chess Game - {current_player.capitalize()}'s turn")
                selected_piece_pos = None
                legal_moves = []

    king_in_check = None
    king_pos = find_king(board_state, current_player)
    if is_in_check(king_pos, board_state, 'black' if current_player == 'white' else 'white'):
        king_in_check = king_pos

    #drawing the board with possible highlighting of the king's square if in check
    draw_board(screen, square_size, board_color_1, board_color_2, king_in_check)
    draw_pieces(screen, square_size, board_state, white_pieces, black_pieces)
    #highlighting legal moves
    if selected_piece_pos and legal_moves:
        highlight_moves(screen, square_size, legal_moves)

    pygame.display.flip()

#game over message handling outside of the main game loop
if game_over and not winner:
    # this condition now only handles checkmate or stalemate, since timeout is handled within the loop
    if is_checkmate(king_pos, board_state, current_player):
        winner = 'Black' if current_player == 'white' else 'White'
        end_game_message = f"Checkmate! {winner} wins!"
    else:
        end_game_message = "Game over! Stalemate or draw."

    display_end_game_message(screen, end_game_message, window_size)

pygame.time.wait(5000)  #keep the message displayed for 5 seconds
pygame.quit()
sys.exit()