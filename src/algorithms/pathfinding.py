"""
Pathfinding algorithms for Half-Edge data structures.
"""
import math
import random
from typing import List, Dict, Optional, Tuple

from ..core.half_edge_ds import HalfEdge, Vertex
from ..core.half_edge import neighbours

def sort(edges: List[HalfEdge]) -> List[HalfEdge]:
    """
    Sort edges by their vertex distances using quicksort.
    
    Args:
        edges: List of edges to sort
        
    Returns:
        Sorted list of edges
    """
    if len(edges) <= 1:
        return edges
        
    pivot = edges[random.randint(0, len(edges) - 1)].V.distance
    small, eq, larger = [], [], []
    
    for edge in edges:
        dist = edge.V.distance
        if dist < pivot:
            small.append(edge)
        elif dist == pivot:
            eq.append(edge)
        else:
            larger.append(edge)
            
    return sort(small) + eq + sort(larger)

def bubblesort(edges: List[HalfEdge], target: HalfEdge) -> None:
    """
    Sort edges by their heuristic value using bubble sort.
    
    Args:
        edges: List of edges to sort
        target: Target edge for heuristic calculation
    """
    for iter_num in range(len(edges)-1, 0, -1):
        for idx in range(iter_num):
            if (edges[idx].V.distance + heuristic(edges[idx], target) > 
                edges[idx+1].V.distance + heuristic(edges[idx+1], target)):
                edges[idx], edges[idx+1] = edges[idx+1], edges[idx]

def dijkstra(start: HalfEdge, target: HalfEdge) -> Dict[int, Optional[int]]:
    """
    Find shortest path using Dijkstra's algorithm.
    
    Args:
        start: Starting edge
        target: Target edge
        
    Returns:
        Dictionary mapping vertex IDs to their previous vertex IDs
    """
    to_visit: List[HalfEdge] = []
    start.V.distance = 0
    came_from: Dict[int, Optional[int]] = {start.V.Vertex_id: None}
    to_visit.append(start)
    
    while to_visit:
        current = to_visit[0]
        del to_visit[0]
        
        if current.V == target.V:
            break
            
        current.V.visited = True
        
        for neighbor in neighbours(current):
            weight = current.V.distance + neighbor.weight if neighbor.weight else 0
            if not neighbor.V.visited or weight < neighbor.V.distance:
                neighbor.V.distance = weight
                if neighbor not in to_visit:
                    to_visit.append(neighbor)
                came_from[neighbor.V.Vertex_id] = current.V.Vertex_id
                
        to_visit = sort(to_visit)
        
    return came_from

def heuristic(edge: HalfEdge, target: HalfEdge) -> float:
    """
    Calculate heuristic value (Euclidean distance) between two edges.
    
    Args:
        edge: Source edge
        target: Target edge
        
    Returns:
        Heuristic value
    """
    return round(math.sqrt(
        (edge.V.getxy()[0] - target.V.getxy()[0])**2 + 
        (edge.V.getxy()[1] - target.V.getxy()[1])**2
    ), 0)

def a_star(start: HalfEdge, target: HalfEdge) -> Dict[int, Optional[int]]:
    """
    Find shortest path using A* algorithm.
    
    Args:
        start: Starting edge
        target: Target edge
        
    Returns:
        Dictionary mapping vertex IDs to their previous vertex IDs
    """
    to_visit: List[HalfEdge] = []
    start.V.distance = 0
    came_from: Dict[int, Optional[int]] = {start.V.Vertex_id: None}
    to_visit.append(start)
    
    while to_visit:
        current = to_visit[0]
        del to_visit[0]
        
        if current.V == target.V:
            break
            
        current.V.visited = True
        
        for neighbor in neighbours(current):
            weight = current.V.distance + neighbor.weight if neighbor.weight else 0
            if not neighbor.V.visited or weight < neighbor.V.distance:
                neighbor.V.distance = weight
                if neighbor not in to_visit:
                    to_visit.append(neighbor)
                came_from[neighbor.V.Vertex_id] = current.V.Vertex_id
                
        bubblesort(to_visit, target)
        
    return came_from

def reconstruct_path(came_from: Dict[int, Optional[int]], 
                    start: int, 
                    goal: int) -> List[int]:
    """
    Reconstruct path from start to goal using came_from dictionary.
    
    Args:
        came_from: Dictionary mapping vertex IDs to their previous vertex IDs
        start: Starting vertex ID
        goal: Goal vertex ID
        
    Returns:
        List of vertex IDs forming the path
    """
    current = goal
    path = []
    
    while current != start:
        path.append(current)
        current = came_from[current]
        
    path.append(start)
    path.reverse()
    return path
