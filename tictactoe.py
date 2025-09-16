import json

DEFAULT_FILE_PATH = "game_state.json"

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_win(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(cell != " " for row in board for cell in row)

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    while True:
        print_board(board)
        try:
            row = int(input(f"Player {current_player}, enter row (0-2): "))
            col = int(input(f"Player {current_player}, enter col (0-2): "))
            if not (0 <= row <= 2 and 0 <= col <= 2):
                print("Row and column must be between 0 and 2.")
                continue
            if board[row][col] != " ":
                print("Cell already taken. Try again.")
                continue
            board[row][col] = current_player
            if check_win(board, current_player):
                print_board(board)
                print(f"Player {current_player} wins!")
                return current_player
            if is_draw(board):
                print_board(board)
                print("It's a draw!")
                return None
            current_player = "O" if current_player == "X" else "X"
        except ValueError:
            print("Invalid input. Please enter numbers 0, 1, or 2.")

def save_game_state(scores, games_played, game_history, file_path=DEFAULT_FILE_PATH):
    game_state = {
        "scores": scores,
        "games_played": games_played,
        "game_history": game_history
    }
    with open(file_path, "w") as file:
        json.dump(game_state, file)
    print(f"Game state saved to {file_path}.")

def load_game_state(file_path=DEFAULT_FILE_PATH):
    try:
        with open(file_path, "r") as file:
            game_state = json.load(file)
        print(f"Game state loaded from {file_path}.")
        return game_state["scores"], game_state["games_played"], game_state["game_history"]
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"No valid saved game state found in {file_path}. Starting fresh.")
        return {"X": 0, "O": 0}, 0, []

def reset_state():
    return {"X": 0, "O": 0}, 0, []

def print_history(game_history):
    print("Game History:")
    if not game_history:
        print("No games played yet.")
    else:
        for record in game_history:
            print(record)

def main():
    file_path = input("Enter the file path to load the game state (or press Enter to use default): ").strip() or DEFAULT_FILE_PATH
    scores, games_played, game_history = load_game_state(file_path)
    while True:
        print(f"Scores: X = {scores['X']}, O = {scores['O']}, Games Played = {games_played}")
        action = input("Choose an option: (p)lay, (r)eset scores, (h)istory, (q)uit: ").lower()
        if action == "p":
            winner = play_game()
            games_played += 1
            if winner:
                scores[winner] += 1
                game_history.append(f"Game {games_played}: Winner - Player {winner}")
            else:
                game_history.append(f"Game {games_played}: Draw")
            save_game_state(scores, games_played, game_history, file_path)
        elif action == "r":
            scores, games_played, game_history = reset_state()
            print("Scores, games played, and history have been reset.")
            save_game_state(scores, games_played, game_history, file_path)
        elif action == "h":
            print_history(game_history)
        elif action == "q":
            print("Thanks for playing!")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()