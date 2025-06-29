import pygame
import time
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 540, 600
CELL_SIZE = WIDTH // 9
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
FONT = pygame.font.SysFont("arial", 36, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 22)
DELAY = 0.02

# Initial state
board = [[0 for _ in range(9)] for _ in range(9)]
locked = [[False for _ in range(9)] for _ in range(9)]
selected = (0, 0)
start_time = None

# Draw grid and board
def draw_grid():
    WIN.fill((245, 245, 245))  # pastel background
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(WIN, (180, 180, 180), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(WIN, (180, 180, 180), (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), thickness)

def draw_board(board, color=None, row=None, col=None):
    draw_grid()
    for i in range(9):
        for j in range(9):
            num = board[i][j]
            if num != 0:
                # Conflict checker coloring
                color_text = (50, 50, 50)
                if not is_valid(board, i, j, num):
                    color_text = (255, 70, 70)
                text = FONT.render(str(num), True, color_text)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                WIN.blit(text, text_rect)

    # Highlight selected cell
    if row is not None and col is not None:
        pygame.draw.rect(WIN, color, (col * CELL_SIZE + 2, row * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4), 3, border_radius=5)

    instructions = SMALL_FONT.render("Click to type | ENTER to solve | C to clear | BACKSPACE to erase", True, (100, 100, 100))
    WIN.blit(instructions, (10, 550))
    pygame.display.update()

# Sudoku logic
def is_valid(board, row, col, num):
    for i in range(9):
        if (board[row][i] == num and i != col) or (board[i][col] == num and i != row):
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            r, c = box_row + i, box_col + j
            if board[r][c] == num and (r, c) != (row, col):
                return False
    return True

def solve(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        draw_board(board, color=(120, 220, 120), row=i, col=j)  # green
                        time.sleep(DELAY)
                        if solve(board):
                            return True
                        board[i][j] = 0
                        draw_board(board, color=(240, 100, 100), row=i, col=j)  # red
                        time.sleep(DELAY)
                return False
    return True

def click_pos(pos):
    x, y = pos
    if x < WIDTH and y < WIDTH:
        return y // CELL_SIZE, x // CELL_SIZE
    return None

def main():
    global selected, start_time
    running = True
    draw_board(board)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = click_pos(pygame.mouse.get_pos())
                if pos:
                    selected = pos

            if event.type == pygame.KEYDOWN:
                r, c = selected
                if event.key == pygame.K_RETURN:
                    # Lock initial values
                    for i in range(9):
                        for j in range(9):
                            if board[i][j] != 0:
                                locked[i][j] = True
                    start_time = time.time()
                    if solve(board):
                        elapsed = time.time() - start_time
                        print(f"Solved in {elapsed:.2f} seconds")
                    else:
                        print("No solution found.")
                elif event.key == pygame.K_BACKSPACE:
                    if not locked[r][c]:
                        board[r][c] = 0
                elif event.key == pygame.K_c:
                    for i in range(9):
                        for j in range(9):
                            board[i][j] = 0
                            locked[i][j] = False
                elif event.unicode in "123456789":
                    if not locked[r][c]:
                        board[r][c] = int(event.unicode)

        draw_board(board, color=(100, 160, 240), row=selected[0], col=selected[1])  # blue

if __name__ == "__main__":
    main()
