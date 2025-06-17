from typing import Union, Tuple, List
from dataclasses import dataclass

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