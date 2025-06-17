"""
Data input/output operations for Half-Edge data structures.
"""
from typing import List, Tuple, Dict
from ..core.half_edge_ds import HalfEdge, Vertex

def get_data(filename: str) -> Tuple[List[HalfEdge], List[Vertex]]:
    """
    Read data from a file and create a Half-Edge data structure.
    
    Args:
        filename: Path to the input file
        
    Returns:
        Tuple containing:
        - List of HalfEdge objects
        - List of Vertex objects
    """
    vertices: List[Vertex] = []
    edges: List[HalfEdge] = []
    vertex_map: Dict[int, Vertex] = {}
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                parts = line.split()
                if not parts:
                    continue
                    
                if parts[0] == 'v':  # Vertex
                    try:
                        # Format: v x y where x and y are floats
                        # Example: v 1.55 70 means x=1.55, y=70
                        x = float(parts[1])
                        y = float(parts[2])
                        
                        vertex = Vertex(x, y, 0.0)  # z-coordinate is 0
                        vertex_map[len(vertices)] = vertex
                        vertices.append(vertex)
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing vertex: {line}")
                        print(f"Error details: {str(e)}")
                        continue
                        
                elif parts[0] == 'f':  # Face
                    try:
                        # Format: f v1 v2 v3 ...
                        # Convert to 0-based indexing
                        vertex_indices = [int(v) - 1 for v in parts[1:]]
                        
                        # Create edges for the face
                        for i in range(len(vertex_indices)):
                            v1 = vertex_map[vertex_indices[i]]
                            v2 = vertex_map[vertex_indices[(i + 1) % len(vertex_indices)]]
                            edge = HalfEdge(v1, v2)
                            edges.append(edge)
                    except (ValueError, IndexError, KeyError) as e:
                        print(f"Error parsing face: {line}")
                        print(f"Error details: {str(e)}")
                        continue
                        
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return [], []
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return [], []
        
    return edges, vertices 