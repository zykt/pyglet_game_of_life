from typing import Any, List


class Board:
    """Universal discrete board class"""
    def __init__(self, width: int, height: int, default: Any=None) -> None:
        self.width: int = width
        self.height: int = height
        self._board: List[List[Any]] = [[default for i in range(width)] for j in range(height)]

    def __getitem__(self, item: int) -> Any:
        return self._board[item]

    def __setitem__(self, key, value):
        raise RuntimeError("Can't modify row directly")

    def __str__(self) -> str:
        formatted_board = '\n'.join(str(row) for row in self._board)
        return f'Board {self.width}x{self.height}:\n{formatted_board}'

    def __repr__(self) -> str:
        formatted_board = '\n'.join(str(row) for row in self._board)
        return f'Board {self.width}x{self.height}:\n{formatted_board}'

