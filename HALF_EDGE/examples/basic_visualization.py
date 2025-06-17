"""
Example usage of the Half-Edge visualization.
"""
from src.core.half_edge import Vertex, HalfEdge
from src.visualization.main import run_visualization

def main():
    # Create some example vertices
    vertices = [
        Vertex(0, 0, 0),
        Vertex(100, 0, 1),
        Vertex(100, 100, 2),
        Vertex(0, 100, 3)
    ]
    
    # Create edges
    edges = [
        HalfEdge(vertices[0], vertices[1]),
        HalfEdge(vertices[1], vertices[2]),
        HalfEdge(vertices[2], vertices[3]),
        HalfEdge(vertices[3], vertices[0])
    ]
    
    # Run visualization
    run_visualization(vertices, edges)

if __name__ == '__main__':
    main()
