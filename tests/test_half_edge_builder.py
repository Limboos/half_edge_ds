import unittest
from src.core.half_edge_builder import HalfEdgeBuilder, EdgeData
from src.core.half_edge import Vertex, HalfEdge
from src.core.validation import VertexValidationError, EdgeValidationError

class TestHalfEdgeBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = HalfEdgeBuilder()
    
    def test_build_simple_triangle(self):
        # Create vertices
        v1 = self.builder.add_vertex(0, 0)
        v2 = self.builder.add_vertex(1, 0)
        v3 = self.builder.add_vertex(0, 1)
        
        # Add edges
        self.builder.add_edge(v1, v2)
        self.builder.add_edge(v2, v3)
        self.builder.add_edge(v3, v1)
        
        # Build the structure
        vertices, edges = self.builder.build()
        
        # Verify the structure
        self.assertEqual(len(vertices), 3)
        self.assertEqual(len(edges), 3)
        
        # Verify edge connections
        for edge in edges:
            self.assertIsNotNone(edge.Sym())
            self.assertIsNotNone(edge.NextV())
    
    def test_build_with_weights(self):
        # Create vertices
        v1 = self.builder.add_vertex(0, 0)
        v2 = self.builder.add_vertex(1, 0)
        
        # Add edge with weight
        self.builder.add_edge(v1, v2, weight=5.0)
        
        # Build the structure
        vertices, edges = self.builder.build()
        
        # Verify weight
        self.assertEqual(edges[0].weight, 5.0)
        self.assertEqual(edges[0].Sym().weight, 5.0)
    
    def test_build_empty(self):
        vertices, edges = self.builder.build()
        self.assertEqual(len(vertices), 0)
        self.assertEqual(len(edges), 0)
    
    def test_invalid_coordinates(self):
        # Test non-numeric coordinates
        with self.assertRaises(VertexValidationError):
            self.builder.add_vertex("0", 0)
        
        # Test NaN coordinates
        with self.assertRaises(VertexValidationError):
            self.builder.add_vertex(float('nan'), 0)
        
        # Test infinite coordinates
        with self.assertRaises(VertexValidationError):
            self.builder.add_vertex(float('inf'), 0)
    
    def test_duplicate_vertices(self):
        # Create first vertex
        v1 = self.builder.add_vertex(0, 0)
        
        # Try to create vertex at same position
        with self.assertRaises(VertexValidationError):
            self.builder.add_vertex(0, 0)
    
    def test_invalid_edge_connections(self):
        # Create vertices
        v1 = self.builder.add_vertex(0, 0)
        v2 = self.builder.add_vertex(1, 0)
        
        # Test self-loop
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v1, v1)
        
        # Test duplicate edge
        self.builder.add_edge(v1, v2)
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v1, v2)
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v2, v1)
    
    def test_invalid_edge_weights(self):
        # Create vertices
        v1 = self.builder.add_vertex(0, 0)
        v2 = self.builder.add_vertex(1, 0)
        
        # Test negative weight
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v1, v2, weight=-1.0)
        
        # Test non-numeric weight
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v1, v2, weight="5.0")
        
        # Test NaN weight
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v1, v2, weight=float('nan'))
        
        # Test infinite weight
        with self.assertRaises(EdgeValidationError):
            self.builder.add_edge(v1, v2, weight=float('inf'))

if __name__ == '__main__':
    unittest.main() 