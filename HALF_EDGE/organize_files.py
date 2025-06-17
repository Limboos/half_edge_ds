"""
Script to organize project files into the proper directory structure.
"""
import os
import shutil
from pathlib import Path

def create_directory(path: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)

def move_file(src: str, dst: str) -> None:
    """Move file from src to dst."""
    if os.path.exists(src):
        shutil.move(src, dst)

def main():
    # Create necessary directories
    create_directory('src/core')
    create_directory('src/algorithms')
    create_directory('src/visualization')
    create_directory('src/utils')
    create_directory('examples')
    create_directory('tests')
    create_directory('data')

    # Move core files
    move_file('Half_Edge_DS.py', 'src/core/half_edge_ds.py')
    move_file('half_edge.py', 'src/core/half_edge.py')
    move_file('cevent.py', 'src/core/cevent.py')

    # Move algorithm files
    move_file('Delauny_Triangulation.py', 'src/algorithms/delaunay.py')
    move_file('path_finding.py', 'src/algorithms/pathfinding.py')
    move_file('otoczka.py', 'src/algorithms/convex_hull.py')

    # Move visualization files
    move_file('GUI.py', 'src/visualization/old_gui.py')
    move_file('Turtle_drawing.py', 'src/visualization/old_turtle.py')

    # Move data files
    for file in ['graph.obj', 'graph.txt', 'graph2.obj', 'graph3.obj', 
                'graph4.obj', 'graph5.obj', 'graph6.obj']:
        move_file(file, f'data/{file}')

    # Move database file
    move_file('data_base.py', 'src/utils/database.py')

    # Create example file
    example_code = '''"""
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
'''
    
    with open('examples/basic_visualization.py', 'w') as f:
        f.write(example_code)

if __name__ == '__main__':
    main() 