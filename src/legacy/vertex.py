from typing import Tuple, Iterator, Optional

class Vertex:
    """
    A class representing a vertex in the half-edge data structure.
    
    Attributes:
        count (int): Class variable for generating unique vertex IDs
        Vertex_id (int): Unique identifier for the vertex
        __x (float): X coordinate
        __y (float): Y coordinate
        __z (float): Z coordinate (defaults to 0)
        visited (bool): Flag indicating if vertex has been visited
        distance (Optional[float]): Distance value for pathfinding algorithms
    """
    count: int = 1

    def __init__(self, x: float, y: float, z: float = 0) -> None:
        """
        Initialize a new vertex.

        Args:
            x (float): X coordinate
            y (float): Y coordinate
            z (float, optional): Z coordinate. Defaults to 0.
        """
        self.Vertex_id: int = Vertex.count
        Vertex.count += 1
        self.__x: float = x
        self.__y: float = y
        self.__z: float = z
        self.visited: bool = False
        self.distance: Optional[float] = None

    def set_visited(self) -> None:
        """Mark the vertex as visited."""
        self.visited = True

    def set_not_visited(self) -> None:
        """Mark the vertex as not visited."""
        self.visited = False

    def getxy(self) -> Tuple[float, float]:
        """
        Get the x and y coordinates of the vertex.

        Returns:
            Tuple[float, float]: (x, y) coordinates
        """
        return self.__x, self.__y

    def set_distance(self, dis: float) -> None:
        """
        Set the distance value for the vertex.

        Args:
            dis (float): Distance value to set
        """
        self.distance = dis

    def __iter__(self) -> Iterator[float]:
        """
        Make the vertex iterable, returning x and y coordinates.

        Returns:
            Iterator[float]: Iterator over [x, y] coordinates
        """
        return iter([self.__x, self.__y])

    def __del__(self) -> None:
        """Cleanup when vertex is deleted."""
        print("deleted") 