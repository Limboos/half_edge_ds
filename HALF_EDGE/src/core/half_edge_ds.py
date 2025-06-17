import math
from typing import List, Optional, Tuple, Union
from dataclasses import dataclass


# TODO
#clean this shit
#update drawing labirary to MathPlotLib


class HalfEdgeValidationError(Exception):
    """Base exception for Half-Edge validation errors."""
    pass

class VertexValidationError(HalfEdgeValidationError):
    """Exception raised for vertex validation errors."""
    pass

class EdgeValidationError(HalfEdgeValidationError):
    """Exception raised for edge validation errors."""
    pass

@dataclass
class ValidationResult:
    """Class for storing validation results."""
    is_valid: bool
    message: str = ""

def validate_coordinates(x: Union[int, float], y: Union[int, float], z: Union[int, float] = 0) -> ValidationResult:
    """Validate vertex coordinates.
    
    Args:
        x: X coordinate
        y: Y coordinate
        z: Z coordinate (default: 0)
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        # Check if coordinates are numeric
        if not all(isinstance(coord, (int, float)) for coord in (x, y, z)):
            return ValidationResult(False, "Coordinates must be numeric values")
        
        # Check for NaN or infinity
        if any(coord != coord or abs(coord) == float('inf') for coord in (x, y, z)):
            return ValidationResult(False, "Coordinates cannot be NaN or infinite")
        
        return ValidationResult(True)
    except Exception as e:
        return ValidationResult(False, f"Coordinate validation error: {str(e)}")

def validate_vertex_id(vertex_id: int, existing_ids: List[int]) -> ValidationResult:
    """Validate vertex ID.
    
    Args:
        vertex_id: ID to validate
        existing_ids: List of existing vertex IDs
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        if not isinstance(vertex_id, int):
            return ValidationResult(False, "Vertex ID must be an integer")
        
        if vertex_id <= 0:
            return ValidationResult(False, "Vertex ID must be positive")
        
        if vertex_id in existing_ids:
            return ValidationResult(False, f"Vertex ID {vertex_id} already exists")
        
        return ValidationResult(True)
    except Exception as e:
        return ValidationResult(False, f"Vertex ID validation error: {str(e)}")

def validate_edge_connection(start_vertex_id: int, end_vertex_id: int, existing_edges: List[Tuple[int, int]]) -> ValidationResult:
    """Validate edge connection.
    
    Args:
        start_vertex_id: ID of the starting vertex
        end_vertex_id: ID of the ending vertex
        existing_edges: List of existing edge connections
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        if start_vertex_id == end_vertex_id:
            return ValidationResult(False, "Cannot create edge to the same vertex")
        
        # Check for duplicate edges
        if (start_vertex_id, end_vertex_id) in existing_edges or (end_vertex_id, start_vertex_id) in existing_edges:
            return ValidationResult(False, f"Edge between vertices {start_vertex_id} and {end_vertex_id} already exists")
        
        return ValidationResult(True)
    except Exception as e:
        return ValidationResult(False, f"Edge connection validation error: {str(e)}")

def validate_edge_weight(weight: Union[int, float, None]) -> ValidationResult:
    """Validate edge weight.
    
    Args:
        weight: Weight to validate
        
    Returns:
        ValidationResult with validation status and message
    """
    try:
        if weight is not None:
            if not isinstance(weight, (int, float)):
                return ValidationResult(False, "Edge weight must be numeric")
            
            if weight < 0:
                return ValidationResult(False, "Edge weight cannot be negative")
            
            if weight != weight or abs(weight) == float('inf'):
                return ValidationResult(False, "Edge weight cannot be NaN or infinite")
        
        return ValidationResult(True)
    except Exception as e:
        return ValidationResult(False, f"Edge weight validation error: {str(e)}")

class Vertex(object):
    """Class representing a vertex in the Half-Edge data structure."""
    count = 1

    def __init__(self, x: float, y: float, z: float = 0):
        """
        Initialize a vertex.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (default: 0)
        """
        self.Vertex_id = Vertex.count
        Vertex.count += 1
        self.__x = x
        self.__y = y
        self.__z = z
        self.visited = False
        self.distance = None

    def set_visited(self) -> None:
        """Mark vertex as visited."""
        self.visited = True

    def set_not_visited(self) -> None:
        """Mark vertex as not visited."""
        self.visited = False

    def getxy(self) -> Tuple[float, float]:
        """Get vertex coordinates."""
        return self.__x, self.__y

    def set_distance(self, dis: float) -> None:
        """Set vertex distance."""
        self.distance = dis

    def __iter__(self):
        return [self.__x, self.__y].__iter__()

    def __del__(self):
        print("deleted")

class HalfEdge(object):
    """Class representing a half-edge in the Half-Edge data structure."""
    count = 1

    def __init__(self, v1: Optional[Vertex] = None, v2: Optional[Vertex] = None):
        """
        Initialize a half-edge.
        
        Args:
            v1: First vertex (optional)
            v2: Second vertex (optional)
        """
        self.id = HalfEdge.count
        HalfEdge.count += 1
        self.V = v1
        self.S = None  # Symmetric edge
        self.Next = None  # Next edge
        self.Prev = None  # Previous edge
        self.taken_edge = False
        self.weight = None
        
        if v1 is not None and v2 is not None:
            self.S = HalfEdge(v2, None)
            self.S.S = self
            self.Next = self
            self.Prev = self
            self.S.Next = self.S
            self.S.Prev = self.S

    def Sym(self) -> 'HalfEdge':
        """Get symmetric half-edge."""
        return self.S

    def NextV(self) -> 'HalfEdge':
        """Get next vertex half-edge."""
        return self.Next

    def next_in(self) -> 'HalfEdge':
        """Get next incoming half-edge."""
        return self.S.Next

    def set_taken(self) -> None:
        """Mark edge as taken."""
        self.taken_edge = True

    def set_not_taken(self) -> None:
        """Mark edge as not taken."""
        self.taken_edge = False

    def get_weight(self) -> Optional[float]:
        """Get edge weight."""
        return self.weight

def MakeEdge(V1: Vertex, V2: Vertex) -> HalfEdge:
    """
    Create an edge between two vertices.
    
    Args:
        V1: First vertex
        V2: Second vertex
        
    Returns:
        Half-edge connecting V1 to V2
    """
    he1 = HalfEdge(V1, V2)
    return he1

def Splice(e1: HalfEdge, e2: HalfEdge) -> None:
    """
    Connect two edges.
    
    Args:
        e1: First half-edge
        e2: Second half-edge
    """
    # Save original connections
    e1_next = e1.Next
    e2_next = e2.Next
    
    # Update Next pointers
    e1.Next = e2_next
    e2.Next = e1_next
    
    # Update Prev pointers
    e1_next.Prev = e2
    e2_next.Prev = e1

def neighbours(edge: HalfEdge) -> List[HalfEdge]:
    """
    Get all neighboring edges of a vertex.
    
    Args:
        edge: Half-edge to get neighbors for
        
    Returns:
        List of neighboring half-edges
    """
    neighbors = []
    current = edge
    
    while True:
        neighbors.append(current)
        current = current.next_in()
        if current == edge:
            break
            
    return neighbors

def Azymut(e):
    # funciton to count angle betwen two vertex
    # this function return an Angle
    # i am useing a Geodesy theory for angel
    x = e.Sym().V.getxy()[0] - e.V.getxy()[0]
    y = e.Sym().V.getxy()[1] - e.V.getxy()[1]

    if x == 0 and y > 0:
        return 0
    elif x == 0 and y < 0:
        return 180
    elif y == 0 and x > 0:
        return 90
    elif y == 0 and x < 0:
        return 270
    else:
        pi = math.degrees(math.atan(math.fabs(x / y)))
        if x > 0 and y > 0:
            pi = pi
        elif x < 0 and y > 0:
            pi = 360 - pi
        elif x < 0 and y < 0:
            pi = 180 + pi
        elif x > 0 and y < 0:
            pi = 180 - pi
    return pi
