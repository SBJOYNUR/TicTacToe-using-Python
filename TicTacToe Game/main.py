import tkinter as tk
from tkinter import messagebox

def main():
    root = tk.Tk()
    root.title("Tic Tac Toe")
    app = TicTacToe(master=root)
    app.mainloop()

class TicTacToe(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.board = [None] * 9
        self.current_player = "X"
        self.game_mode = None  # "HUMANvsAI" or "AIvsAI"
        self.is_game_over = False
        self.move_delay = 1000  # Delay in milliseconds

    def create_widgets(self):
        self.buttons = []
        for i in range(9):
            button = tk.Button(self, text='', font=('Comic Sans MS', 20), height=3, width=6,
                               command=lambda i=i: self.make_move(i))
            
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)
        
        self.mode_label = tk.Label(self, text="Please Select Game Mode:", font=('normal', 14))
        self.mode_label.grid(row=3, column=0, columnspan=3)
        self.hvai_button = tk.Button(self, text="Human vs AI", command=lambda: self.set_mode("HUMANvsAI"))
        self.hvai_button.grid(row=4, column=0, columnspan=3)
        self.aivai_button = tk.Button(self, text="AI vs AI", command=lambda: self.set_mode("AIvsAI"))
        self.aivai_button.grid(row=5, column=0, columnspan=3)


    def set_mode(self, mode):
        self.game_mode = mode
        self.mode_label.config(text=f"Mode: {mode}")
        self.reset_game()


    def make_move(self, index):
        if self.board[index] is None and not self.is_game_over:
            self.update_board(index, self.current_player)
            if self.game_mode == "HUMANvsAI" and self.current_player == "O":
                self.master.after(self.move_delay, self.ai_move)


    def update_board(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player)
        print_board(self.board)  # Print the board to console
        if check_winner(self.board, player):
            messagebox.showinfo("Game Over", f"Hurrey!! Player {player} wins!")
            self.is_game_over = True
            return
        if None not in self.board:
            messagebox.showinfo("Game Over", "Oops!..It's a draw!")
            self.is_game_over = True
            return
        self.current_player = "O" if self.current_player == "X" else "X"
        if self.game_mode == "AIvsAI" and not self.is_game_over:
            self.master.after(self.move_delay, self.ai_move)


    def ai_move(self):
        # Minimax algorithm as before
        best_score = float('-inf')
        best_move = None
        for i in range(len(self.board)):
            if self.board[i] is None:
                self.board[i] = self.current_player
                score = minimax(self.board, False, float('-inf'), float('inf'))
                self.board[i] = None
                if score > best_score:
                    best_score = score
                    best_move = i
        self.update_board(best_move, self.current_player)


    def reset_game(self):
        self.board = [None] * 9
        for button in self.buttons:
            button.config(text='')
        self.current_player = "X"
        self.is_game_over = False
        if self.game_mode == "AIvsAI":
            self.master.after(self.move_delay, self.ai_move)


def print_board(board):
    for i in range(0, 9, 3):
        print(board[i:i+3])

def check_winner(board, player):
    wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)]
    return any(all(board[i] == player for i in win) for win in wins)

def minimax(board, is_maximizing, alpha, beta):
    current_player = "O" if is_maximizing else "X"
    winner = None
    if check_winner(board, "X"):
        winner = "X"
    elif check_winner(board, "O"):
        winner = "O"

    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif None not in board:
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(len(board)):
            if board[i] is None:
                board[i] = "O"
                score = minimax(board, False, alpha, beta)
                board[i] = None
                best_score = max(score, best_score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
        return best_score
    else:
        best_score = float('inf')
        for i in range(len(board)):
            if board[i] is None:
                board[i] = "X"
                score = minimax(board, True, alpha, beta)
                board[i] = None
                best_score = min(score, best_score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
        return best_score

if __name__ == "__main__":
    main()
