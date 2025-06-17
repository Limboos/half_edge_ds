from typing import Optional
from .edge import HalfEdge

class Face:
    """
    A class representing a face in the half-edge data structure.
    
    Attributes:
        count (int): Class variable for generating unique face IDs
        id (int): Unique identifier for the face
        edge (Optional[HalfEdge]): A half-edge on the boundary of this face
    """
    count: int = 1

    def __init__(self) -> None:
        """Initialize a new face."""
        self.id: int = Face.count
        Face.count += 1
        self.edge: Optional[HalfEdge] = None

    def set_edge(self, edge: HalfEdge) -> None:
        """
        Set a boundary edge for this face.

        Args:
            edge (HalfEdge): A half-edge on the boundary of this face
        """
        self.edge = edge 