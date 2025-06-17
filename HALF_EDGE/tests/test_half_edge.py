import pytest
from src.core.half_edge import Vertex, HalfEdge, Face, Fast_splice, verify_connectivity

def test_vertex_creation():
    """Test vertex creation and properties"""
    v = Vertex(1.0, 2.0)
    assert v.x == 1.0
    assert v.y == 2.0
    assert v.edge is None

def test_half_edge_creation():
    """Test half-edge creation and basic properties"""
    v1 = Vertex(0.0, 0.0)
    v2 = Vertex(1.0, 1.0)
    e = HalfEdge(v1)
    e.twin = HalfEdge(v2)
    e.twin.twin = e
    
    assert e.vertex == v1
    assert e.twin.vertex == v2
    assert e.twin.twin == e
    assert e.next is None
    assert e.face is None

def test_face_creation():
    """Test face creation and edge-face relationships"""
    # Create three vertices
    v1 = Vertex(0.0, 0.0)
    v2 = Vertex(1.0, 0.0)
    v3 = Vertex(0.0, 1.0)
    
    # Create edges
    e1 = HalfEdge(v1)
    e2 = HalfEdge(v2)
    e3 = HalfEdge(v3)
    
    # Create face
    f = Face()
    f.edge = e1
    
    # Set up edge-face relationships
    e1.face = f
    e2.face = f
    e3.face = f
    
    # Set up next pointers
    e1.next = e2
    e2.next = e3
    e3.next = e1
    
    assert f.edge == e1
    assert e1.face == f
    assert e2.face == f
    assert e3.face == f
    assert e1.next == e2
    assert e2.next == e3
    assert e3.next == e1

def test_fast_splice():
    """Test Fast_splice function with a simple triangle"""
    # Create three vertices
    v1 = Vertex(0.0, 0.0)
    v2 = Vertex(1.0, 0.0)
    v3 = Vertex(0.0, 1.0)
    
    # Create edges
    e1 = HalfEdge(v1)
    e2 = HalfEdge(v2)
    e3 = HalfEdge(v3)
    
    # Create twin edges
    e1_twin = HalfEdge(v2)
    e2_twin = HalfEdge(v3)
    e3_twin = HalfEdge(v1)
    
    # Set up twin relationships
    e1.twin = e1_twin
    e1_twin.twin = e1
    e2.twin = e2_twin
    e2_twin.twin = e2
    e3.twin = e3_twin
    e3_twin.twin = e3
    
    # Create list of edges
    edges = [e1, e2, e3, e1_twin, e2_twin, e3_twin]
    
    # Perform Fast_splice
    Fast_splice(edges)
    
    # Verify connectivity
    assert verify_connectivity(edges)
    
    # Verify next pointers
    assert e1.next == e2
    assert e2.next == e3
    assert e3.next == e1
    assert e1_twin.next == e3_twin
    assert e3_twin.next == e2_twin
    assert e2_twin.next == e1_twin

def test_verify_connectivity():
    """Test connectivity verification"""
    # Create a valid triangle
    v1 = Vertex(0.0, 0.0)
    v2 = Vertex(1.0, 0.0)
    v3 = Vertex(0.0, 1.0)
    
    e1 = HalfEdge(v1)
    e2 = HalfEdge(v2)
    e3 = HalfEdge(v3)
    
    e1.next = e2
    e2.next = e3
    e3.next = e1
    
    f = Face()
    f.edge = e1
    e1.face = f
    e2.face = f
    e3.face = f
    
    edges = [e1, e2, e3]
    
    # Test valid connectivity
    assert verify_connectivity(edges)
    
    # Test invalid connectivity (broken next pointer)
    e2.next = None
    assert not verify_connectivity(edges)
    
    # Test invalid connectivity (missing face)
    e2.next = e3
    e2.face = None
    assert not verify_connectivity(edges) 