import pyglet
from board import Board


class Cell:
    DEAD = 0
    ALIVE = 1


def neighbors(board: Board, x: int, y: int) -> int:
    """Count neighbors of x, y on board"""
    n = 0

    def border_check(x_, y_):
        """Helper for determining whether given x_ and y_ are valid"""
        return 0 <= x_ < board.width and 0 <= y_ < board.height

    # for each offset in [-1; 1]
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if border_check(x + i, y + j):
                    n += 1 if board[x+i][y+j] == Cell.ALIVE else 0
    return n


def turn(board: Board) -> Board:
    """Calculate next turn in game of Life"""
    new_board = Board(board.width, board.height)
    for w in range(board.width):
        for h in range(board.height):
            neighbor_count = neighbors(board, w, h)
            if neighbor_count == 3:
                new_board[w][h] = Cell.ALIVE
            elif neighbor_count == 2 and board[w][h] == Cell.ALIVE:
                new_board[w][h] = Cell.ALIVE
            else:
                new_board[w][h] = Cell.DEAD
    return new_board


def board_batch(board: Board, x, y, x_size, y_size) -> pyglet.graphics.Batch:
    """Create batch of vertices from board for later rendering"""
    batch = pyglet.graphics.Batch()
    width_coef = x_size // board.width
    height_coef = y_size // board.height

    for w in range(board.width):
        for h in range(board.height):
            colours = (255, 255, 255) * 4 if board[w][h] == Cell.ALIVE else (0, 0, 0) * 4
            batch.add(4, pyglet.gl.GL_QUADS, None,
                      ('v2i', (x + w * width_coef + 1, y + h * height_coef + 1,
                               x + w * width_coef + 1, y + (h+1) * height_coef - 1,
                               x + (w+1) * width_coef - 1, y + (h+1) * height_coef - 1,
                               x + (w+1) * width_coef - 1, y + h * height_coef + 1)),
                      ('c3B', colours))
    return batch


window = pyglet.window.Window()
board = Board(8, 8, Cell.DEAD)
board[4][2] = Cell.ALIVE
board[4][3] = Cell.ALIVE
board[4][4] = Cell.ALIVE
# board[3][3] = Cell.ALIVE
# board[3][4] = Cell.ALIVE
print(board)
print(neighbors(board, 1, 2))
def helper(dt):
    """Horrible hack to hook up Game of Life to pyglet clock"""
    global board
    board = turn(board)
    # print("Turn!")
    # print(board)
pyglet.clock.schedule_interval(helper, 1)


@window.event
def on_draw() -> None:
    """Redraws screen every time it's called"""
    window.clear()
    batch = board_batch(board, 10, 10, 400, 400)
    batch.draw()


def main() -> None:
    pyglet.app.run()


if __name__ == '__main__':
    main()
