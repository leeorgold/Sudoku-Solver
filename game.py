import pygame
from board import Board
from random import randrange

pygame.init()
SQUARE_LENGTH = 50
SQUARE_NUM = 9
WIN_LEN = SQUARE_LENGTH * SQUARE_NUM
SPACING = 10
WIN_SIZE = (WIN_LEN + 2 * SPACING, WIN_LEN + SQUARE_LENGTH + 2 * SPACING)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 100)
FONT = pygame.font.Font(None, 50)

clock = pygame.time.Clock()
FPS = 5
screen = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Sudoku")

selected = None
mistakes = 0
finish = False


def get_board() -> list[list[int | str]]:
    """The function picks a random board."""
    if randrange(2) == 0:
        return [[6, '.', '.', '.', 2, '.', 1, '.', '.'],
                ['.', '.', '.', '.', 9, '.', 8, '.', 3],
                ['.', 8, 1, 5, '.', '.', '.', 7, '.'],
                [3, '.', '.', 4, '.', '.', '.', '.', 6],
                ['.', '.', 9, 2, '.', 3, '.', '.', '.'],
                [5, '.', '.', '.', '.', 7, '.', '.', 1],
                ['.', 2, '.', '.', '.', 8, 7, '.', '.'],
                [7, '.', 6, '.', 4, '.', '.', '.', '.'],
                ['.', '.', 4, '.', 7, '.', '.', '.', 2]]
    else:
        return [[5, 3, '.', '.', 7, '.', '.', '.', '.'],
                [6, '.', '.', 1, 9, 5, '.', '.', '.'],
                ['.', 9, 8, '.', '.', '.', '.', 6, '.'],
                [8, '.', '.', '.', 6, '.', '.', '.', 3],
                [4, '.', '.', 8, '.', 3, '.', '.', 1],
                [7, '.', '.', '.', 2, '.', '.', '.', 6],
                ['.', 6, '.', '.', '.', '.', 2, 8, '.'],
                ['.', '.', '.', 4, 1, 9, '.', '.', 5],
                ['.', '.', '.', '.', 8, '.', '.', 7, 9]]


BOARD_ROWS = get_board()


def select(x, y):
    """The function gets the mouse position and selects the matched square on the board."""
    global selected
    x -= SPACING
    y -= SPACING
    x //= SQUARE_LENGTH
    y //= SQUARE_LENGTH
    if not 0 <= x <= 8 or not 0 <= y <= 8 or BOARD_ROWS[y][x] != '.':
        selected = None
    else:
        selected = (x, y)


def draw_selected():
    """The function highlights the selected square."""
    x, y = selected
    x *= SQUARE_LENGTH
    y *= SQUARE_LENGTH
    x += SPACING
    y += SPACING
    pygame.draw.rect(screen, YELLOW, (x, y, SQUARE_LENGTH, SQUARE_LENGTH))
    # pygame.draw.rect(screen, RED, (x, y, SQUARE_LENGTH, SQUARE_LENGTH), 3)


def draw_mistakes():
    """The function writes the number of mistakes."""
    text = FONT.render(f'Mistakes: {mistakes}', True, RED)
    screen.blit(text, (SPACING, WIN_LEN + 2 * SPACING))


def get_thickness(i):
    """The function gets the number of line in the grid and returns the matched thickness."""
    return 1 if i % 3 != 0 else 3


def draw_grid():
    """The function draws the grid on the screen."""
    # screen.fill(WHITE)
    for i in range(SQUARE_NUM + 1):
        pygame.draw.line(screen, BLACK, (SPACING + i * SQUARE_LENGTH, SPACING),
                         (SPACING + i * SQUARE_LENGTH, WIN_LEN + SPACING), get_thickness(i))
    for i in range(SQUARE_NUM + 1):
        pygame.draw.line(screen, BLACK, (SPACING, SPACING + i * SQUARE_LENGTH),
                         (SPACING + WIN_LEN, SPACING + i * SQUARE_LENGTH), get_thickness(i))


def write_values():
    """The function adds the numbers to the screen."""
    for y, row in enumerate(BOARD_ROWS):
        for x, val in enumerate(row):
            if val != '.':
                text = FONT.render(str(val), True, BLACK)
                screen.blit(text, (x * SQUARE_LENGTH + 15 + SPACING, y * SQUARE_LENGTH + 10 + SPACING))


def you_won():
    """the function displays a 'You Won!' message on the screen."""
    text = FONT.render('You Won!', True, GREEN)
    screen.blit(text, (SPACING + WIN_LEN - 155, WIN_LEN + 2 * SPACING))


def main():
    global mistakes, selected, finish

    running = False
    while not running:
        for event in pygame.event.get():

            # user pressed X
            if event.type == pygame.QUIT:
                running = True
                break

            # user pressed the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN and not finish:
                select(*pygame.mouse.get_pos())

            # user tries to add a value to the board. 49 means 1 and 57 means 9.
            elif event.type == pygame.KEYDOWN and selected and not finish and 49 <= event.key <= 57:
                BOARD_ROWS[selected[1]][selected[0]] = event.key - 48

                # check the new board and if it is solved
                try:
                    board = Board(BOARD_ROWS)
                    finish = board.is_solved()

                # the new board is invalid
                except AssertionError as e:
                    BOARD_ROWS[selected[1]][selected[0]] = '.'
                    print(e)
                    mistakes += 1

                # the new board is valid
                else:
                    # there are no possible solutions to new board
                    if not board.solve():
                        print('No possible solution.')
                        BOARD_ROWS[selected[1]][selected[0]] = '.'
                        mistakes += 1

                finally:
                    selected = None

        screen.fill(WHITE)

        if selected:
            draw_selected()
        if finish:
            you_won()

        draw_grid()
        write_values()
        draw_mistakes()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
