"""
Main visualization module for Half-Edge data structures.
"""
import sys
import argparse
import logging
from typing import List, Tuple, Set

from src.core.half_edge_ds import Vertex, HalfEdge, MakeEdge, Splice
from src.core.half_edge_builder import HalfEdgeBuilder
from .gui import run_visualization
from .turtle_visualizer import TurtleVisualizer

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

def load_data_from_file(filename: str) -> tuple[List[Vertex], List[HalfEdge]]:
    """
    Load vertices and edges from a file.
    
    Args:
        filename: Path to the file containing the data
        
    Returns:
        Tuple of (vertices, edges)
    """
    builder = HalfEdgeBuilder()
    added_edges: Set[Tuple[int, int]] = set()  # Set to track added edges
    
    try:
        with open(filename, 'r') as f:
            # First pass: collect all vertices to find min/max coordinates
            temp_vertices = []
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                parts = line.split()
                if not parts:
                    continue
                    
                if parts[0] == 'v':  # Vertex
                    try:
                        # Format: v x.y where x and y are coordinates
                        # Example: v 1.55 means x=1, y=55
                        coords = parts[1].split('.')
                        x = float(coords[0])
                        y = float(coords[1])
                        temp_vertices.append((x, y))
                    except (ValueError, IndexError) as e:
                        logging.error(f"Error parsing vertex: {line} | {e}")
                        continue
            
            # Calculate min/max coordinates
            if temp_vertices:
                min_x = min(x for x, _ in temp_vertices)
                max_x = max(x for x, _ in temp_vertices)
                min_y = min(y for _, y in temp_vertices)
                max_y = max(y for _, y in temp_vertices)
                
                # Calculate center and scale
                center_x = (min_x + max_x) / 2
                center_y = (min_y + max_y) / 2
                scale = 400 / max(max_x - min_x, max_y - min_y) if max_x != min_x or max_y != min_y else 1
                
                # Reset file pointer to beginning
                f.seek(0)
                
                # Second pass: create vertices with centered coordinates
                vertex_map = {}  # Map to store vertices by their index
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                        
                    parts = line.split()
                    if not parts:
                        continue
                        
                    if parts[0] == 'v':  # Vertex
                        try:
                            # Format: v x.y where x and y are coordinates
                            coords = parts[1].split('.')
                            x = float(coords[0])
                            y = float(coords[1])
                            
                            # Center and scale coordinates
                            x = (x - center_x) * scale + 400  # Center horizontally
                            y = (y - center_y) * scale + 300  # Center vertically
                            
                            # Add vertex to builder
                            builder.add_vertex(x, y, 0.0)
                            vertex_map[len(vertex_map)] = builder._vertices[-1]
                        except (ValueError, IndexError) as e:
                            logging.error(f"Error parsing vertex: {line} | {e}")
                            continue
                            
                    elif parts[0] == 'f':  # Face
                        try:
                            # Convert to 0-based indexing
                            vertex_indices = [int(v) - 1 for v in parts[1:]]
                            
                            # Add edges for the face
                            for i in range(len(vertex_indices)):
                                v1 = vertex_map[vertex_indices[i]]
                                v2 = vertex_map[vertex_indices[(i + 1) % len(vertex_indices)]]
                                
                                # Check if edge already exists (in either direction)
                                edge_key = (v1.Vertex_id, v2.Vertex_id)
                                reverse_key = (v2.Vertex_id, v1.Vertex_id)
                                
                                if edge_key not in added_edges and reverse_key not in added_edges:
                                    builder.add_edge(v1, v2)
                                    added_edges.add(edge_key)
                        except (ValueError, IndexError, KeyError) as e:
                            logging.error(f"Error parsing face: {line} | {e}")
                            continue
                
    except FileNotFoundError:
        logging.error(f"Error: File {filename} not found")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        sys.exit(1)
        
    # Build the complete Half-Edge structure
    vertices, edges = builder.build()
    
    logging.debug(f"[main] Builder returned {len(vertices)} vertices and {len(edges)} edges")
    
    if not vertices or not edges:
        logging.error("Error: No data loaded")
        sys.exit(1)
        
    return vertices, edges

def main():
    """
    Main function to run the visualization.
    """
    parser = argparse.ArgumentParser(description='Half-Edge Visualization')
    parser.add_argument('--file', type=str, required=True, help='Input file path')
    parser.add_argument('--mode', type=str, default='gui', choices=['gui', 'turtle'],
                      help='Visualization mode (default: gui)')
    
    args = parser.parse_args()
    
    # Load data
    vertices, edges = load_data_from_file(args.file)
    
    print(f"Loaded {len(vertices)} vertices and {len(edges)} edges")
    print(f"Visualization mode: {args.mode}")
    
    # Run visualization
    if args.mode == 'gui':
        run_visualization(vertices, edges)
    else:
        visualizer = TurtleVisualizer()
        visualizer.run(edges[0], vertices)

if __name__ == '__main__':
    main() 