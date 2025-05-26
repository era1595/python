import numpy as np
import random
import time
import math
import sys
import itertools
import tkinter as tk
from tkinter import simpledialog, messagebox, font

# --- Game Constants ---
HUMAN_PLAYER = 'X'
COMPUTER_PLAYER = 'O'
EMPTY = ' '

# --- Game Settings (to be taken from GUI) ---
DIMENSIONS = 3  # Default
BOARD_SIZE = 3  # Default
WIN_LENGTH = 3  # Default
MAX_DEPTH = 3   # Default

def get_nd_coordinates(index, shape):
    """ Converts a flat index to N-dimensional coordinates. (NumPy already does this)"""
    return np.unravel_index(index, shape)

def get_flat_index(coords, shape):
    """ Converts N-dimensional coordinates to a flat index. (NumPy already does this)"""
    return np.ravel_multi_index(coords, shape)

def is_within_bounds(coords, shape):
    """Checks if the given coordinates are within the board boundaries."""
    return all(0 <= c < s for c, s in zip(coords, shape))

# --- Board Functions ---

def create_board(dimensions, board_size):
    """Creates an empty game board (NumPy array) with the specified dimensions."""
    shape = tuple([board_size] * dimensions)
    return np.full(shape, EMPTY, dtype=str)

def print_board_nd(board):
    """Attempts to print the N-dimensional board."""
    dims = board.ndim
    size = board.shape[0] # Assuming all dimensions are equal

    print("\n--- Board Status ---")
    if dims == 2:
        for i in range(size):
            print(" | ".join(board[i, :]))
            if i < size - 1:
                print("---" * size)
    elif dims == 3:
        print("(Displayed in layers)")
        for layer in range(size):
            print(f"\nLayer {layer}:")
            for row in range(size):
                print(" | ".join(board[layer, row, :]))
                if row < size - 1:
                    print("---" * size)
    else: # Visualization is difficult for 4+ dimensions
        print(f"({dims}-dimensional board - only filled cells are listed)")
        it = np.nditer(board, flags=['multi_index'])
        found_any = False
        while not it.finished:
            if it[0] != EMPTY:
                print(f"  Coordinate {it.multi_index}: {it[0]}")
                found_any = True
            it.iternext()
        if not found_any:
             print("  (Board is empty)")
    print("--------------------\n")

def get_available_moves_nd(board):
    """Returns the N-dimensional coordinates of empty squares."""
    available = []
    it = np.nditer(board, flags=['multi_index'])
    while not it.finished:
        if it[0] == EMPTY:
            available.append(it.multi_index)
        it.iternext()
    return available

def is_board_full_nd(board):
    """Checks if the board is full."""
    return EMPTY not in board

# --- Winning Check (N-Dimensional) ---


def check_winner_nd(board, player):
    dims = board.ndim
    shape = board.shape
    # print(f"Debug: check_winner_nd called - Player: {player}") # Can be added for debugging

    # Create all possible direction vectors (combinations of -1, 0, 1, excluding (0,0,...))
    directions = list(itertools.product([-1, 0, 1], repeat=dims))
    directions.remove(tuple([0] * dims)) # Remove the zero vector

    it = np.nditer(board, flags=['multi_index'])
    while not it.finished: # **** FIX: Loop condition should be 'it.finished' ****
        start_coord = it.multi_index
        if board[start_coord] == player: # Only start with the player's own piece
            for direction in directions:
                count = 0
                for i in range(WIN_LENGTH):
                    # Calculate the current coordinate
                    current_coord_list = [sc + i * d for sc, d in zip(start_coord, direction)]
                    current_coord = tuple(current_coord_list)

                    # Check boundaries and player
                    if is_within_bounds(current_coord, shape) and board[current_coord] == player:
                        count += 1
                    else:
                        break # Line is broken

                if count == WIN_LENGTH:
                    # print(f"Debug: Winning line found! Start: {start_coord}, Direction: {direction}, Player: {player}") # Can be added for debugging
                    return True # Winner found

        it.iternext() # **** FIX: Iterator should be advanced at the end of the loop ****

    # print(f"Debug: No winner found - Player: {player}") # Can be added for debugging
    return False # No winner

# --- Player Moves ---

def get_human_move_nd(board):
    """Gets a valid N-dimensional move from the human or catches the 'LB' debug command."""
    dims = board.ndim
    size = board.shape[0]
    while True:
        try:
            coord_str = input(f"Your turn ({HUMAN_PLAYER}). Enter {dims} coordinates (e.g., 0,1,2) or type 'LB': ")
            # Check for debug command
            if coord_str.strip().upper() == 'LB':
                return "LB" # Return a special string

            # Process normal coordinates
            coords = tuple(int(c.strip()) for c in coord_str.split(','))

            if len(coords) != dims:
                print(f"Error: Please enter {dims} coordinates.")
                continue

            if not is_within_bounds(coords, board.shape):
                print(f"Error: Coordinates must be between 0 and {size-1}.")
                continue

            if board[coords] == EMPTY:
                return coords # Return the coordinate tuple
            else:
                print("This square is full. Choose another square.")

        except ValueError:
            print("Invalid input. Enter coordinates as numbers separated by commas, or type 'LB'.")
        except Exception as e:
            print(f"An error occurred: {e}")

def get_random_computer_move_nd(board):
    """Selects a random valid N-dimensional move for the computer."""
    available = get_available_moves_nd(board)
    print("Computer is thinking (Random)...")
    time.sleep(0.5)
    if available:
        return random.choice(available)
    return None # If no empty spots

# --- Minimax Algorithm (N-Dimensional, Depth Limited) ---

def evaluate_board_nd(board):
    """Evaluates the state of the N-dimensional board for Minimax."""
    if check_winner_nd(board, COMPUTER_PLAYER):
        return 10
    elif check_winner_nd(board, HUMAN_PLAYER):
        return -10
    else:
        return 0 # Draw or game ongoing

def minimax_nd(board, depth, is_maximizing, alpha, beta, max_depth_limit):
    """N-Dimensional Minimax (Alpha-Beta Pruning and Depth Limited)."""
    score = evaluate_board_nd(board)

    # Terminal states or depth limit
    if score == 10: return score - depth # Faster win is better
    if score == -10: return score + depth # Later loss is better
    if is_board_full_nd(board): return 0
    if depth == max_depth_limit: return evaluate_board_nd(board) # Return score at depth limit

    available_moves = get_available_moves_nd(board)
    if not available_moves: # If no moves left (rarely falls here, but good to check)
         return 0

    if is_maximizing: # Computer (maximizing player)
        best_score = -math.inf
        # We can shuffle moves for speed (optional)
        # random.shuffle(available_moves)
        for move in available_moves:
            board[move] = COMPUTER_PLAYER
            current_score = minimax_nd(board, depth + 1, False, alpha, beta, max_depth_limit)
            board[move] = EMPTY # Undo
            best_score = max(best_score, current_score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break # Beta pruning
        return best_score
    else: # Human (minimizing player)
        best_score = math.inf
        # random.shuffle(available_moves)
        for move in available_moves:
            board[move] = HUMAN_PLAYER
            current_score = minimax_nd(board, depth + 1, True, alpha, beta, max_depth_limit)
            board[move] = EMPTY # Undo
            best_score = min(best_score, current_score)
            beta = min(beta, best_score)
            if beta <= alpha:
                break # Alpha pruning
        return best_score

def get_best_computer_move_nd(board, max_depth_limit):
    """Finds the best N-dimensional move for the computer using Minimax.
       (Prioritizes urgent blocks)"""
    best_score = -math.inf
    best_move = None
    available_moves = get_available_moves_nd(board) # All empty squares

    if not available_moves:
        return None

    # --- Heuristic: Prioritize Urgent Blocks ---
    human_winning_moves = get_human_winning_moves(board) # Where can human win?
    direct_blocking_moves = [] # Direct blocking moves computer can play

    if human_winning_moves:
        print(f"DEBUG (get_best_move): Human threats ({len(human_winning_moves)}): {human_winning_moves}")
        # Which of the current empty squares are human's winning squares?
        direct_blocking_moves = [move for move in available_moves if move in human_winning_moves]

        if direct_blocking_moves:
            print(f"DEBUG (get_best_move): Direct blocking moves found: {direct_blocking_moves}")
            # Run Minimax ONLY on these blocking moves!
            print(f"DEBUG (get_best_move): Minimax is running only on blocking moves...")
            available_moves_to_check = direct_blocking_moves # Restrict search space
        else:
            # If no direct blocking move (maybe human created a double threat, etc.)
            # continue to check all moves
            print("DEBUG (get_best_move): No direct blocking move, all moves will be evaluated.")
            available_moves_to_check = available_moves # Use all empty squares
    else:
        # If no human threat, check all empty squares
        available_moves_to_check = available_moves

    # --- Minimax Loop (with Restricted or Full Search Space) ---
    print(f"Computer is thinking deeply (Minimax Depth {max_depth_limit} - {len(available_moves_to_check)} moves)... This may take a while...")
    start_time = time.time()

    for move in available_moves_to_check: # Only look at moves to be checked
        board[move] = COMPUTER_PLAYER
        move_score = minimax_nd(board, 0, False, -math.inf, math.inf, max_depth_limit)
        board[move] = EMPTY # Undo move

        # print(f"Debug: Move {move} Score: {move_score}") # For debugging

        if move_score > best_score:
            best_score = move_score
            best_move = move
        # If scores are equal, we can choose randomly (optional)
        elif move_score == best_score and random.choice([True, False]):
            best_move = move

    end_time = time.time()
    print(f"Thinking time: {end_time - start_time:.2f} seconds.")

    # If no "good" move is found among the checked moves
    # (this can happen especially if the search space is restricted)
    # or if Minimax somehow returns None
    if best_move is None:
        # If there were originally empty moves, choose randomly from them
        if available_moves: # Use the original full list
            print("Computer couldn't find a valid strategy (or got stuck in restricted search), playing randomly.")
            best_move = random.choice(available_moves)
        else:
             # If there were no empty moves initially (very rare)
             best_move = None

    return best_move

# --- Special Mode Functions (N-Dimensional) ---

def check_imminent_loss_nd(board, player_to_check):
    """
    Checks if the opponent can win on the next move (N-Dimensional).
    Returns True if they can.
    """
    opponent = HUMAN_PLAYER if player_to_check == COMPUTER_PLAYER else COMPUTER_PLAYER
    available_moves = get_available_moves_nd(board)
    for move in available_moves:
        board[move] = opponent # Try opponent's move
        if check_winner_nd(board, opponent):
            board[move] = EMPTY # Undo
            return True # Yes, opponent can win on the next move
        board[move] = EMPTY # Undo
    return False # Opponent cannot win on the next move

def get_human_winning_moves(board):
    """Returns a list of coordinates of empty squares where the human can win on the next move."""
    winning_moves = []
    opponent = HUMAN_PLAYER # We are checking for human's win
    available_moves = get_available_moves_nd(board)
    for move in available_moves:
        board[move] = opponent # Try human's move
        if check_winner_nd(board, opponent):
            winning_moves.append(move) # This move wins
        board[move] = EMPTY # Undo
    return winning_moves

def last_breathe_warning_nd():
    """Eerie warning for Last Breathe mode (N-Dimensional)."""
    print("\n" + "*"*50)
    print("!!! WARNING: LAST BREATHE MODE ACTIVE !!!")
    print(f"EVEN IN THIS {DIMENSIONS}-DIMENSIONAL UNIVERSE, THE END IS NIGH...")
    print("But rules are made to be bent!")
    print("LET CHAOS BEGIN!")
    print("*"*50 + "\n")
    time.sleep(2.5)

def last_breathe_manipulate_nd(board):
    """
    Manipulates the board 'as it wishes' in 'Last Breathe' mode.
    Strategy: Tries to win ruthlessly or sabotages the opponent.
    (Strategy 2 V3 - Deletes the X that poses the most threats)
    """
    print("\n!!! REALITY IS COLLAPSING !!!")
    time.sleep(1)
    print("THE BOARD BENDS TO MY WILL!")
    time.sleep(1.5)

    new_board = board.copy()
    dims = new_board.ndim
    shape = new_board.shape
    available_moves = get_available_moves_nd(new_board)

    # --- Strategy 1: Can the computer win instantly? ---
    for move in available_moves:
        new_board[move] = COMPUTER_PLAYER
        if check_winner_nd(new_board, COMPUTER_PLAYER):
            print("...I HAVE WRITTEN YOUR FATE MYSELF!")
            time.sleep(1)
            return new_board
        new_board[move] = EMPTY
    print("DEBUG (Manip): Strategy 1 (Instant Win) failed.")

    # --- Strategy 2 (Improved V3): Delete the X that poses the most threats ---
    human_wins = get_human_winning_moves(new_board)
    if human_wins:
        print(f"DEBUG (Manip): Strategy 2 V3 - Human threats detected: {human_wins}")

        x_threat_count = {} # Count how many threat lines each X is part of
        all_winning_line_details = {} # To store detailed info (optional)

        directions = list(itertools.product([-1, 0, 1], repeat=dims))
        directions.remove(tuple([0] * dims))
        unique_directions = []
        seen_opposites = set()
        for d_check in directions:
            opposite_d = tuple(-x for x in d_check)
            if d_check not in seen_opposites:
                unique_directions.append(d_check)
                seen_opposites.add(opposite_d)

        # For each potential winning square, find and count associated Xs
        for target_coord in human_wins:
            threat_lines_found_for_target = 0 # How many lines found for this target?
            for d in unique_directions:
                coords_before = []
                count_before = 0
                for i in range(1, WIN_LENGTH):
                    check_coord = tuple(tc - i * dr for tc, dr in zip(target_coord, d))
                    if is_within_bounds(check_coord, shape) and new_board[check_coord] == HUMAN_PLAYER:
                        count_before += 1; coords_before.append(check_coord)
                    else: break

                coords_after = []
                count_after = 0
                for i in range(1, WIN_LENGTH):
                    check_coord = tuple(tc + i * dr for tc, dr in zip(target_coord, d))
                    if is_within_bounds(check_coord, shape) and new_board[check_coord] == HUMAN_PLAYER:
                        count_after += 1; coords_after.append(check_coord)
                    else: break

                if count_before + count_after + 1 >= WIN_LENGTH:
                    threat_lines_found_for_target += 1
                    current_line_xs = list(set(coords_before + coords_after))
                    all_winning_line_details[(target_coord, d)] = current_line_xs # Store details
                    # Increment threat counter for each X in this line
                    for x_coord in current_line_xs:
                        x_threat_count[x_coord] = x_threat_count.get(x_coord, 0) + 1
                    # Important: If a target square is won by multiple lines
                    # (e.g., corner), associated Xs can be counted multiple times. This is desired.

            # if threat_lines_found_for_target == 0:
            #      print(f"WARNING (Manip): No threat line found for {target_coord}!")

        print(f"DEBUG (Manip): X Threat Counter: {x_threat_count}")

        coord_to_remove = None
        # Find the X that poses the most threats
        if x_threat_count:
            max_threats = 0 # Start from 0
            # Find the max threat count
            for count in x_threat_count.values():
                if count > max_threats:
                    max_threats = count

            # Find Xs with the max threat count
            if max_threats > 0:
                 best_xs_to_remove = [x for x, count in x_threat_count.items() if count == max_threats]
                 print(f"DEBUG (Manip): Highest Threat Count: {max_threats}, Candidates: {best_xs_to_remove}")
                 coord_to_remove = random.choice(best_xs_to_remove) # Choose one of the candidates
            else:
                 print("DEBUG (Manip): Threat counter exists but max threat is 0? Fallback...")
                 # Fallback in this case

        # If a logical X to remove was found
        if coord_to_remove:
            print(f"DEBUG (Manip): {coord_to_remove} will be removed (most threatening).")
            new_board[coord_to_remove] = EMPTY
            print(f"...I am deleting your biggest threat at coordinate {coord_to_remove}!")
            time.sleep(1)
            return new_board # Return the modified board
        else:
             # If X to remove was not found (either no threat or couldn't be counted) -> Fallback
             print(f"DEBUG (Manip): Logical X not found (V3)! Fallback: Directly filling first target ({human_wins[0] if human_wins else 'None'}).")
             if human_wins: # Fallback only makes sense if there's a threat
                 target_coord = human_wins[0] # Take the first threat
                 if new_board[target_coord] == EMPTY:
                      new_board[target_coord] = COMPUTER_PLAYER # Block directly
                      print(f"...I am blocking your target {target_coord}!")
                      time.sleep(1)
                      return new_board
                 else:
                      print(f"DEBUG (Manip): Fallback target {target_coord} already full (V3)? Proceeding to Strategy 3.")
                      pass # Continue to Strategy 3
             else:
                  # Shouldn't get here if no threat, but for safety
                  print("DEBUG (Manip): Cannot fallback, there was no human threat.")
                  pass # Continue to Strategy 3
    else:
         print("DEBUG (Manip): Strategy 2 V3 - No immediate human threat found.")


    # --- Strategy 3: Randomly turn an 'X' into an 'O' ---
    # (This strategy kicks in if there's no urgent threat or it can't be blocked)
    print("DEBUG (Manip): Trying Strategy 3 (X -> O conversion).")
    x_coords = [idx for idx, val in np.ndenumerate(new_board) if val == HUMAN_PLAYER]
    if x_coords:
        coord_to_flip = random.choice(x_coords)
        new_board[coord_to_flip] = COMPUTER_PLAYER
        print("...I am absorbing your power into mine!")
        time.sleep(1)
        return new_board
    print("DEBUG (Manip): Strategy 3 failed (No X to flip).")


    # --- Strategy 4: Randomly place an 'O' ---
    print("DEBUG (Manip): Trying Strategy 4 (Random O placement).")
    # available_moves was taken at the beginning of the function
    if available_moves:
        coord_to_place = random.choice(available_moves)
        new_board[coord_to_place] = COMPUTER_PLAYER
        print("...I am putting my signature on the universe!")
        time.sleep(1)
        return new_board
    print("DEBUG (Manip): Strategy 4 failed (No empty space).")


    # --- Last Resort ---
    print("DEBUG (Manip): All manipulation strategies exhausted. Board unchanged.")
    print("...I am preserving order for now.")
    return board # Return the original board (before copying)


#-------------------------------------------------------------
# GUI Class
#-------------------------------------------------------------
class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title(f"{DIMENSIONS}D Tic-Tac-Toe")
        # self.master.geometry("400x500") # Size can be adjusted

        # Style
        self.button_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=12)
        self.layer_font = font.Font(family="Helvetica", size=10, weight="bold")
        self.normal_bg = "#F0F0F0" # Button background
        self.lb_bg = "#550000" # Last Breathe background (dark red)
        self.lb_fg = "white" # Last Breathe text color

        # Game Variables
        self.board = None
        self.buttons = {} # To store GUI buttons {(z,y,x): button}
        self.current_player = HUMAN_PLAYER
        self.game_over = False
        self.last_breathe_active = False
        self.last_breathe_potential = False
        self.consecutive_computer_losses = 0
        self.human_score = 0
        self.computer_score = 0
        self.ties = 0

        # Main Frame
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Status and Score Panel (Top)
        self.status_frame = tk.Frame(self.main_frame)
        self.status_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.status_label = tk.Label(self.status_frame, text="Welcome to the Game!", font=self.status_font, height=2)
        self.status_label.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(self.status_frame, text="Score: You 0 - Computer 0 (D: 0)", font=self.status_font)
        self.score_label.pack(side=tk.RIGHT, padx=10)

        # Board Frame (Center)
        self.board_outer_frame = tk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=2)
        self.board_outer_frame.pack(side=tk.TOP, pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Control Buttons (Bottom)
        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        self.new_game_button = tk.Button(self.control_frame, text="New Game", command=self.start_new_game)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.settings_button = tk.Button(self.control_frame, text="Settings", command=self.change_settings)
        self.settings_button.pack(side=tk.LEFT, padx=10)

        # Ask for settings at start and initialize the game
        self.ask_settings()
        self.start_new_game()

    def ask_settings(self):
        global DIMENSIONS, BOARD_SIZE, WIN_LENGTH, MAX_DEPTH
        try:
            # Currently supports only 2D and 3D
            d = simpledialog.askinteger("Dimension Selection", "How many dimensions for the game? (2 or 3)", parent=self.master, minvalue=2, maxvalue=3, initialvalue=DIMENSIONS)
            if d is None: return # Cancelled
            DIMENSIONS = d

            s = simpledialog.askinteger("Board Size", f"How many squares per side of each dimension? ({DIMENSIONS} entered)", parent=self.master, minvalue=2, maxvalue=5, initialvalue=BOARD_SIZE) # Limit max to 5
            if s is None: return
            BOARD_SIZE = s

            WIN_LENGTH = BOARD_SIZE # Usually same as board size

            depth = simpledialog.askinteger("AI Difficulty (Minimax Depth)", "How deep should the AI look? (e.g., 2-4)\nHigher values slow down.", parent=self.master, minvalue=1, maxvalue=5, initialvalue=MAX_DEPTH)
            if depth is None: return
            MAX_DEPTH = depth

            self.master.title(f"{DIMENSIONS}D Tic-Tac-Toe ({BOARD_SIZE}x{BOARD_SIZE})")

        except Exception as e:
            messagebox.showerror("Settings Error", f"Error getting settings: {e}")
            # Revert to defaults
            DIMENSIONS, BOARD_SIZE, WIN_LENGTH, MAX_DEPTH = 3, 3, 3, 3
            self.master.title(f"{DIMENSIONS}D Tic-Tac-Toe ({BOARD_SIZE}x{BOARD_SIZE})")

    def change_settings(self):
        self.ask_settings()
        self.start_new_game() # Start new game when settings change

    def create_board_gui(self):
        # Clear previous board interface
        for widget in self.board_outer_frame.winfo_children():
            widget.destroy()
        self.buttons = {}

        if DIMENSIONS == 2:
            board_frame = tk.Frame(self.board_outer_frame)
            board_frame.pack(expand=True)
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    coord = (r, c) # 2D coordinate
                    button = tk.Button(board_frame, text=EMPTY, font=self.button_font,
                                       width=4, height=2, relief=tk.RAISED, borderwidth=2,
                                       command=lambda c=coord: self.handle_click(c))
                    button.grid(row=r, column=c, padx=2, pady=2)
                    self.buttons[coord] = button
        elif DIMENSIONS == 3:
            # Create a frame for each layer
            for layer_idx in range(BOARD_SIZE):
                layer_frame = tk.Frame(self.board_outer_frame, relief=tk.GROOVE, borderwidth=1, padx=5, pady=5)
                layer_frame.pack(side=tk.TOP, pady=5) # Stack layers vertically

                tk.Label(layer_frame, text=f"Layer {layer_idx}", font=self.layer_font).pack(side=tk.TOP)

                grid_frame = tk.Frame(layer_frame)
                grid_frame.pack(side=tk.TOP)

                for r in range(BOARD_SIZE):
                    for c in range(BOARD_SIZE):
                        coord = (layer_idx, r, c) # 3D coordinate
                        button = tk.Button(grid_frame, text=EMPTY, font=self.button_font,
                                           width=3, height=1, relief=tk.RAISED, borderwidth=1,
                                           command=lambda c=coord: self.handle_click(c))
                        button.grid(row=r, column=c, padx=1, pady=1)
                        self.buttons[coord] = button
        else:
            # No support for 4D+ for now, show a message
            tk.Label(self.board_outer_frame, text=f"Visual interface not supported for {DIMENSIONS}D.", font=self.status_font).pack(expand=True)

    def start_new_game(self):
        self.board = create_board(DIMENSIONS, BOARD_SIZE)
        self.current_player = HUMAN_PLAYER
        self.game_over = False
        self.last_breathe_active = False
        # last_breathe_potential is set based on loss count from previous game
        self.last_breathe_potential = (self.consecutive_computer_losses >= 2)

        self.update_status("New Game Started. Your Turn (X).")
        self.update_score_label()
        self.create_board_gui() # Create/reset GUI board
        self.enable_board()
        self.update_gui_board() # Clear content
        self.set_background(self.normal_bg) # Normal background

        if self.last_breathe_potential:
             self.update_status("Computer is nervous... Your Turn (X).")

    def handle_click(self, coords):
        if self.game_over or self.current_player != HUMAN_PLAYER:
            return # Ignore click if game is over or it's computer's turn

        if self.board[coords] == EMPTY:
            # Human Move
            self.board[coords] = HUMAN_PLAYER
            self.buttons[coords].config(text=HUMAN_PLAYER, state=tk.DISABLED, fg='blue') # Update button

            # Check for Win/Draw
            if check_winner_nd(self.board, HUMAN_PLAYER):
                self.handle_game_over(winner=HUMAN_PLAYER)
            elif is_board_full_nd(self.board):
                self.handle_game_over(winner=None) # Draw
            else:
                # Computer's Turn
                self.current_player = COMPUTER_PLAYER
                self.update_status("Computer's Turn (O)...")
                self.disable_board() # So human can't click again
                # Start AI move with a small delay (for UI to update)
                self.master.after(200, self.computer_turn)
        else:
            self.update_status("This square is full! Choose another place.")

    def computer_turn(self):
        if self.game_over: return

        move_to_make = None
        perform_manipulation = False
        best_move_candidate = None
        manipulation_message = "" # Store manipulation message

        # --- 1. Last Breathe Activation Check ---
        if self.last_breathe_potential and not self.last_breathe_active:
            self.update_status("Computer is thinking (LB Activation Check)...")
            self.master.update_idletasks() # Ensure message is visible
            if check_imminent_loss_nd(self.board, COMPUTER_PLAYER):
                self.last_breathe_active = True
                # Show warning in status label instead of messagebox
                self.update_status("!!! LAST BREATHE ACTIVE !!!")
                self.set_background(self.lb_bg, self.lb_fg) # Change background
                messagebox.showwarning("Last Breathe!", "Computer is cornered!\nLAST BREATHE mode active!", parent=self.master) # Additional warning
            else:
                self.update_status("Computer is thinking (LB Potential)...")

        # --- 2. Move Selection and Manipulation (If LB Active) ---
        if self.last_breathe_active:
            self.update_status("Computer is thinking deeply (Last Breathe!)...")
            self.master.update_idletasks()
            best_move_candidate = get_best_computer_move_nd(self.board, MAX_DEPTH) # This can still freeze!

            should_manipulate = False
            if best_move_candidate:
                self.board[best_move_candidate] = COMPUTER_PLAYER
                if check_imminent_loss_nd(self.board, COMPUTER_PLAYER):
                    should_manipulate = True
                self.board[best_move_candidate] = EMPTY
            elif check_imminent_loss_nd(self.board, COMPUTER_PLAYER): # Didn't find a move but threat exists
                 should_manipulate = True

            if should_manipulate:
                 self.update_status("!!! REALITY IS COLLAPSING !!!")
                 self.master.update_idletasks()
                 time.sleep(1.5) # Dramatic effect
                 # Manipulation function can return a message (default for now)
                 temp_board_before = self.board.copy()
                 manipulated_board = last_breathe_manipulate_nd(temp_board_before) # Run on a copy
                 self.board = manipulated_board # Update the actual board
                 perform_manipulation = True
                 manipulation_message = "Board manipulated!" # Simple message
                 # TODO: It would be better to update last_breathe_manipulate_nd to return a message.
                 self.update_status(manipulation_message)
                 self.update_gui_board() # Refresh GUI
            else:
                 move_to_make = best_move_candidate # No manipulation, make Minimax move

        # --- 3. Move Selection (If LB Not Active) ---
        if not self.last_breathe_active and not perform_manipulation:
            if self.last_breathe_potential: # Potential exists but not active -> Minimax
                self.update_status("Computer is thinking (Minimax - Risky)...")
                self.master.update_idletasks()
                move_to_make = get_best_computer_move_nd(self.board, MAX_DEPTH) # Can freeze
            else: # Normal Game -> Random
                self.update_status("Computer is thinking (Random)...")
                self.master.update_idletasks()
                move_to_make = get_random_computer_move_nd(self.board) # Fast

        # --- 4. Make the Move (If manipulation was not performed) ---
        if not perform_manipulation:
            if move_to_make and self.board[move_to_make] == EMPTY:
                self.board[move_to_make] = COMPUTER_PLAYER
                # Update GUI
                self.buttons[move_to_make].config(text=COMPUTER_PLAYER, state=tk.DISABLED, fg='red')
                print(f"Computer played {move_to_make}.") # Log to console
            elif move_to_make: # Error: Full square or other issue
                 print(f"ERROR (computer_turn): move_to_make is full or invalid: {move_to_make}")
                 # Emergency: Find a random empty square
                 alt_move = get_random_computer_move_nd(self.board)
                 if alt_move and self.board[alt_move] == EMPTY:
                      self.board[alt_move] = COMPUTER_PLAYER
                      self.buttons[alt_move].config(text=COMPUTER_PLAYER, state=tk.DISABLED, fg='red')
                      print(f"Alternatively played {alt_move}.")
                 else:
                     print("ERROR: Alternative move could not be found!")
                     # Game is likely a draw or locked
                     if not self.game_over and is_board_full_nd(self.board):
                          self.handle_game_over(winner=None)

            else: # Minimax/Random couldn't find a move (Board full?)
                 print("Computer couldn't find a move.")
                 if not self.game_over and is_board_full_nd(self.board):
                     self.handle_game_over(winner=None)


        # --- 5. End of Turn Checks ---
        if not self.game_over: # If manipulation/move didn't end the game
            winner = None
            if perform_manipulation: # Check after manipulation
                if check_winner_nd(self.board, COMPUTER_PLAYER): winner = COMPUTER_PLAYER
                elif check_winner_nd(self.board, HUMAN_PLAYER): winner = HUMAN_PLAYER
                elif is_board_full_nd(self.board): winner = None # Draw
            else: # Check after normal move
                 if check_winner_nd(self.board, COMPUTER_PLAYER): winner = COMPUTER_PLAYER
                 elif is_board_full_nd(self.board): winner = None # Draw

            if winner == COMPUTER_PLAYER:
                self.handle_game_over(winner=COMPUTER_PLAYER)
            elif winner is None and is_board_full_nd(self.board):
                 self.handle_game_over(winner=None)
            elif winner == HUMAN_PLAYER: # If human wins after manipulation
                 self.handle_game_over(winner=HUMAN_PLAYER)

        # If game continues, give turn to human
        if not self.game_over:
            self.current_player = HUMAN_PLAYER
            if not perform_manipulation: # Only message after normal move
                 self.update_status(f"Computer played {move_to_make if move_to_make else '?'}. Your turn (X).")
            elif manipulation_message:
                 self.update_status(f"{manipulation_message} Your turn (X).")
            else: # If manipulation happened but no special message
                 self.update_status("Your turn (X).")

            self.enable_board() # So human can play

    def update_status(self, message):
        self.status_label.config(text=message)

    def update_score_label(self):
        score_text = f"Score: You {self.human_score} - PC {self.computer_score} (D: {self.ties})"
        self.score_label.config(text=score_text)

    def update_gui_board(self):
        """Updates GUI buttons according to the current board array."""
        if not self.board is None:
            it = np.nditer(self.board, flags=['multi_index'])
            while not it.finished:
                coords = it.multi_index
                player = str(it[0]) # Get string from NumPy array
                button = self.buttons.get(coords)
                if button:
                    color = 'blue' if player == HUMAN_PLAYER else 'red' if player == COMPUTER_PLAYER else 'black'
                    state = tk.DISABLED if player != EMPTY else tk.NORMAL
                    button.config(text=player, fg=color, state=state)
                it.iternext()

    def disable_board(self):
        for button in self.buttons.values():
            button.config(state=tk.DISABLED)

    def enable_board(self):
        # Only enable empty squares
        for coords, button in self.buttons.items():
             if self.board[coords] == EMPTY:
                button.config(state=tk.NORMAL)
             else:
                button.config(state=tk.DISABLED)


    def set_background(self, bg_color, fg_color="black"):
         """Sets the background of the main window and important frames."""
         self.master.config(bg=bg_color)
         self.main_frame.config(bg=bg_color)
         self.status_frame.config(bg=bg_color)
         # Set background and text color of labels
         for label in [self.status_label, self.score_label]:
              label.config(bg=bg_color, fg=fg_color)
         # Active/passive colors of buttons are managed separately,
         # but maybe we can change button appearance in last breathe too.

    def handle_game_over(self, winner):
        self.game_over = True
        self.disable_board()
        self.set_background(self.normal_bg) # Revert to normal color

        message = ""
        if winner == HUMAN_PLAYER:
            message = "🎉 Congratulations, You Won! 🎉"
            self.human_score += 1
            self.consecutive_computer_losses += 1
        elif winner == COMPUTER_PLAYER:
            message = "😞 Computer Won! 😞"
            self.computer_score += 1
            self.consecutive_computer_losses = 0 # Streak broken
        else: # Draw
            message = "🤝 Game Draw! 🤝"
            self.ties += 1
            self.consecutive_computer_losses = 0 # Streak broken

        self.update_status(message)
        self.update_score_label()
        print(f"Game over. Consecutive losses: {self.consecutive_computer_losses}") # Console log

        # Play again?
        if messagebox.askyesno("Game Over", f"{message}\nDo you want to play again?", parent=self.master):
            self.start_new_game()
        else:
            self.master.quit() # Close the UI


# --- Start Main Application ---
if __name__ == "__main__":
    # Check for required library
    try:
        import numpy
    except ImportError:
        print("Error: 'numpy' library is required for this game.")
        print("Please install it with 'pip install numpy' command.")
        sys.exit(1)

    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
