from typing import Optional
from .vertex import Vertex
import logging

logger = logging.getLogger(__name__)

class HalfEdge:
    """
    A class representing a half-edge in the half-edge data structure.
    
    Attributes:
        count (int): Class variable for generating unique edge IDs
        id (int): Unique identifier for the edge
        V (Optional[Vertex]): The vertex at the origin of this half-edge
        S (Optional['HalfEdge']): The symmetric half-edge
        N (Optional['HalfEdge']): The next half-edge in the face
        taken_edge (bool): Flag indicating if edge has been processed
        weight (Optional[float]): Weight of the edge for pathfinding
    """
    count: int = 1

    def __init__(self) -> None:
        """Initialize a new half-edge."""
        self.id: int = HalfEdge.count
        HalfEdge.count += 1
        self.V: Optional[Vertex] = None
        self.S: Optional['HalfEdge'] = None
        self.N: Optional['HalfEdge'] = None
        self.taken_edge: bool = False
        self.weight: Optional[float] = None

    def Sym(self) -> 'HalfEdge':
        """
        Get the symmetric half-edge.

        Returns:
            HalfEdge: The symmetric half-edge
        """
        return self.S

    def NextV(self) -> 'HalfEdge':
        """
        Get the next half-edge in the face.

        Returns:
            HalfEdge: The next half-edge
        """
        return self.N

    def next_in(self) -> 'HalfEdge':
        """
        Get the next half-edge in the incident face.

        Returns:
            HalfEdge: The next half-edge in the incident face
        """
        return self.S.N

    def set_taken(self) -> None:
        """Mark the edge as taken."""
        self.taken_edge = True

    def set_not_taken(self) -> None:
        """Mark the edge as not taken."""
        self.taken_edge = False

    def get_weight(self) -> Optional[float]:
        """
        Get the weight of the edge.

        Returns:
            Optional[float]: The weight of the edge
        """
        return self.weight


def MakeEdge(V1: Vertex, V2: Vertex) -> HalfEdge:
    """
    Create a new edge between two vertices.

    Args:
        V1 (Vertex): First vertex
        V2 (Vertex): Second vertex

    Returns:
        HalfEdge: The first half-edge of the created edge
    """
    he1 = HalfEdge()
    he2 = HalfEdge()
    he1.V = V1
    he1.S = he2
    he1.N = he1
    he2.V = V2
    he2.S = he1
    he2.N = he2
    logger.debug(f"MakeEdge: Created edge {he1.id} from {V1.Vertex_id} to {V2.Vertex_id} and its sym {he2.id} from {V2.Vertex_id} to {V1.Vertex_id}")
    return he1


def Splice(e1: HalfEdge, e2: HalfEdge) -> None:
    """
    Connect two edges by updating their next pointers.

    Args:
        e1 (HalfEdge): First half-edge
        e2 (HalfEdge): Second half-edge
    """
    temp = e1.N
    e1.N = e2.N
    e2.N = temp
    logger.debug(f"Splice: Connected edge {e1.id} (V={e1.V.Vertex_id}) with edge {e2.id} (V={e2.V.Vertex_id})") 