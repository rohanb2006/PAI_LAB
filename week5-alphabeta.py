class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def print_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))
            if i < 6:
                print("-----")

    def is_winner(self, player):
        # Rows
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] == player:
                return True

        # Columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] == player:
                return True

        # Diagonals
        if self.board[0] == self.board[4] == self.board[8] == player:
            return True
        if self.board[2] == self.board[4] == self.board[6] == player:
            return True

        return False

    def is_full(self):
        return ' ' not in self.board

    def is_game_over(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_full()

    def get_available_moves(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def make_move(self, move):
        self.board[move] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def undo_move(self, move):
        self.board[move] = ' '
        self.current_player = 'O' if self.current_player == 'X' else 'X'


# ----------------------
# Alpha-Beta Algorithm
# ----------------------

def alpha_beta(game, alpha, beta, is_maximizing):
    if game.is_winner('O'):
        return 1
    if game.is_winner('X'):
        return -1
    if game.is_full():
        return 0

    if is_maximizing:
        max_eval = -float('inf')
        for move in game.get_available_moves():
            game.make_move(move)
            eval = alpha_beta(game, alpha, beta, False)
            game.undo_move(move)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:   # Pruning
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.get_available_moves():
            game.make_move(move)
            eval = alpha_beta(game, alpha, beta, True)
            game.undo_move(move)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:   # Pruning
                break
        return min_eval

def get_best_move(game):
    best_score = -float('inf')
    best_move = None

    for move in game.get_available_moves():
        game.make_move(move)
        score = alpha_beta(game, -float('inf'), float('inf'), False)
        game.undo_move(move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


# ----------------------
# Play Game
# ----------------------

game = TicTacToe()

while not game.is_game_over():
    game.print_board()

    if game.current_player == 'X':
        try:
            move = int(input("Enter your move (0-8): "))
            if move not in game.get_available_moves():
                print("Invalid move! Try again.")
                continue
            game.make_move(move)
        except ValueError:
            print("Enter a valid number (0-8)")
    else:
        print("AI is thinking...")
        move = get_best_move(game)
        print("AI plays:", move)
        game.make_move(move)

game.print_board()

if game.is_winner('X'):
    print("You win!")
elif game.is_winner('O'):
    print("AI wins!")
else:
    print("It's a draw!")
