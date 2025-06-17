from typing import List, Tuple, Optional
from dataclasses import dataclass
from .half_edge_ds import (
    HalfEdge, Vertex, MakeEdge, Splice, Azymut,
    validate_coordinates, validate_vertex_id, validate_edge_connection,
    validate_edge_weight, VertexValidationError, EdgeValidationError
)
import logging

logger = logging.getLogger(__name__)

@dataclass
class EdgeData:
    """Data class for storing edge information during building."""
    start_vertex: Vertex
    end_vertex: Vertex
    weight: Optional[float] = None

class HalfEdgeBuilder:
    """Builder class for creating Half-Edge data structures."""
    
    def __init__(self):
        self._edges: List[EdgeData] = []
        self._vertices: List[Vertex] = []
        self._built_edges: List[HalfEdge] = []
        self._existing_vertex_ids: List[int] = []
        self._existing_edges: List[Tuple[int, int]] = []
    
    def add_vertex(self, x: float, y: float, z: float = 0) -> 'HalfEdgeBuilder':
        """Add a vertex to the structure.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (default: 0)
            
        Returns:
            self for method chaining
            
        Raises:
            VertexValidationError: If coordinates are invalid
        """
        # Validate coordinates
        coord_validation = validate_coordinates(x, y, z)
        if not coord_validation.is_valid:
            raise VertexValidationError(coord_validation.message)
        
        # Create and validate vertex
        vertex = Vertex(x, y, z)
        id_validation = validate_vertex_id(vertex.Vertex_id, self._existing_vertex_ids)
        if not id_validation.is_valid:
            raise VertexValidationError(id_validation.message)
        
        self._vertices.append(vertex)
        self._existing_vertex_ids.append(vertex.Vertex_id)
        return self
    
    def add_edge(self, start_vertex: Vertex, end_vertex: Vertex, weight: Optional[float] = None) -> 'HalfEdgeBuilder':
        """Add an edge between two vertices.
        
        Args:
            start_vertex: Starting vertex
            end_vertex: Ending vertex
            weight: Optional weight for the edge
            
        Returns:
            self for method chaining
            
        Raises:
            EdgeValidationError: If edge connection or weight is invalid
        """
        # Validate edge connection
        edge_validation = validate_edge_connection(
            start_vertex.Vertex_id,
            end_vertex.Vertex_id,
            self._existing_edges
        )
        if not edge_validation.is_valid:
            raise EdgeValidationError(edge_validation.message)
        
        # Validate weight if provided
        weight_validation = validate_edge_weight(weight)
        if not weight_validation.is_valid:
            raise EdgeValidationError(weight_validation.message)
        
        edge_data = EdgeData(start_vertex, end_vertex, weight)
        self._edges.append(edge_data)
        self._existing_edges.append((start_vertex.Vertex_id, end_vertex.Vertex_id))
        return self
    
    def build(self) -> Tuple[List[Vertex], List[HalfEdge]]:
        """Build the Half-Edge data structure.
        
        Returns:
            Tuple containing list of vertices and list of half-edges
        """
        # Create all edges
        for edge_data in self._edges:
            he = MakeEdge(edge_data.start_vertex, edge_data.end_vertex)
            if edge_data.weight is not None:
                he.weight = edge_data.weight
                he.Sym().weight = edge_data.weight
            self._built_edges.append(he)
        
        # Connect edges using Fast_splice
        self._connect_edges()
        logger.debug(f"[HalfEdgeBuilder] Built {len(self._vertices)} vertices and {len(self._built_edges)} edges")
        for e in self._built_edges:
            logger.debug(f"[HalfEdgeBuilder] Edge: {e.V.Vertex_id} -> {e.S.V.Vertex_id}")
        return self._vertices, self._built_edges
    
    def _connect_edges(self) -> None:
        """Internal method to connect edges using Fast_splice algorithm."""
        # Create vertex to edge mapping
        v_id = {}
        for edge in self._built_edges:
            v_id.update({edge.V.Vertex_id: []})
            v_id.update({edge.Sym().V.Vertex_id: []})
        
        # Add edges to vertex mapping
        for edge in self._built_edges:
            v_id[edge.V.Vertex_id].append(edge)
            v_id[edge.Sym().V.Vertex_id].append(edge.Sym())
        
        # Connect edges
        for vertex_id, vertex_edges in v_id.items():
            if len(vertex_edges) > 1:
                # Create list of [angle, edge] pairs
                A = []
                for edge in vertex_edges:
                    A.append([Azymut(edge), edge])
                
                # Sort by angle
                A.sort()
                
                # Connect edges
                if len(A) == 2:
                    logger.debug(f"Fast_splice: Splicing two edges at vertex {vertex_id}: {A[0][1].id}, {A[1][1].id}")
                    Splice(A[1][1], A[0][1])
                else:
                    for i in range(len(A) - 1):
                        logger.debug(f"Fast_splice: Splicing edge {A[0][1].id} with edge {A[i+1][1].id} at vertex {vertex_id}")
                        Splice(A[0][1], A[i + 1][1])
                
                logger.debug(f"Connected {len(vertex_edges)} edges at vertex {vertex_id}")
                # Log the order of edges for debugging
                edge_order = [f"{e[1].V.Vertex_id}->{e[1].S.V.Vertex_id}" for e in A]
                logger.debug(f"Edge order at vertex {vertex_id}: {' -> '.join(edge_order)}") 