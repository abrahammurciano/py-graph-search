from pygraphsearch import Edge, Node
from typing import Collection, Iterable, Optional
from .Move import Move


class Board(Node):
    """Represents a square board of dimensions n by n.

    Each tile in the board contains a number from 0 to n, where 0 is the empty tile. The empty tile may be swapped with any tile directly adjacent to it.
    """

    def __init__(
        self,
        size: int,
        tiles: Collection[int],
        __empty_tile_index: Optional[int] = None,
    ):
        """Construct an n by n board with the given tiles.

        Args:
            size (int): The number of tiles per row or column.
            tiles (Collection[int]): A collection of the integers to use for the tiles.

        Raises:
            ValueError: If n is not positive or if the number of tiles provided is not equal to n^2.
        """
        if size <= 0 or (tiles and len(tiles) != size * size):
            raise ValueError(
                "n must be positive and the size of tiles must be equal to n^2."
            )
        self.__size = size
        self.__tiles = list(tiles or range(size * size))
        if __empty_tile_index is None:
            self.__empty_tile = self.__tiles.index(0)
        else:
            self.__empty_tile = __empty_tile_index

    @property
    def size(self):
        """The number of tiles per row or column."""
        return self.__size

    def neighbours(self) -> Iterable[Edge["Board"]]:
        neighbours = []
        for move in Move:
            if self.can_move(move):
                edge = Edge[Board](self, self.move(move))
                neighbours.append(edge)
                edge_move_map[edge] = move
        return neighbours

    def can_move(self, move: Move) -> bool:
        """Check if the empty tile can be moven in the given direction.

        Args:
            move (Move): The direction to move the empty tile.

        Returns:
            bool: True if the empty tile can be moved in the given direction, False otherwise.
        """
        if move == Move.UP:
            return self.__empty_tile >= self.size
        elif move == Move.DOWN:
            return self.__empty_tile < self.size * (self.size - 1)
        elif move == Move.LEFT:
            return self.__empty_tile % self.size != 0
        else:
            return self.__empty_tile % self.size != self.size - 1

    def move(self, move: Move) -> "Board":
        """Create a copy of the board with the empty tile moved one space in the given direction.

        Args:
            move (Move): The direction to move the empty tile.

        Returns:
            Board: The board after the move.

        Raises:
            RuntimeError: If the empty tile cannot be moved in the given direction.
        """
        if not self.can_move(move):
            raise RuntimeError("The empty tile cannot be moved in the given direction.")
        if move == Move.UP:
            new_empty_tile = self.__empty_tile - self.size
        elif move == Move.DOWN:
            new_empty_tile = self.__empty_tile + self.size
        elif move == Move.LEFT:
            new_empty_tile = self.__empty_tile - 1
        else:
            new_empty_tile = self.__empty_tile + 1
        new_tiles = self.__tiles.copy()
        new_tiles[new_empty_tile], new_tiles[self.__empty_tile] = (
            new_tiles[self.__empty_tile],
            new_tiles[new_empty_tile],
        )
        return Board(self.size, new_tiles, new_empty_tile)

    def __eq__(self, board: object) -> bool:
        return isinstance(board, Board) and self.__tiles == board.__tiles

    def __hash__(self) -> int:
        return hash(tuple(self.__tiles))

    def __str__(self):
        return "\n".join(
            [
                " ".join(str(tile) for tile in self.__tiles[start : start + self.size])
                for start in range(0, len(self.__tiles), self.size)
            ]
        )


edge_move_map: dict[Edge[Board], Move] = {}
