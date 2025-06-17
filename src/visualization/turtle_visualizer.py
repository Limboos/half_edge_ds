"""
Turtle-based visualization module for Half-Edge data structures.
Provides interactive visualization capabilities using Python's turtle graphics.
"""
from typing import List, Tuple, Optional
import turtle
from turtle import Turtle
import math

from ..core.half_edge_ds import HalfEdge, Vertex

class TurtleVisualizer:
    """A class for visualizing Half-Edge data structures using turtle graphics."""
    
    def __init__(self):
        """Initialize the turtle visualizer."""
        self.turtle = Turtle()
        self.turtle.speed(0)
        self.drawing_edge: Optional[HalfEdge] = None
        self.taken_edge: Optional[HalfEdge] = None
        self.main_edge: Optional[HalfEdge] = None
        self.setup_turtle()

    def setup_turtle(self) -> None:
        """Set up turtle graphics environment."""
        turtle.onkey(self.next_edge, 'Up')
        turtle.onkey(self.prev_edge, 'Down')
        turtle.onkey(self.sym_edge, 's')
        turtle.onkey(self.exit_screen, 'q')
        turtle.onscreenclick(self.click_on_edge, 1)
        turtle.onscreenclick(self.add_point, 3)
        turtle.listen()

    def draw_delaunay_triangulation(self, drawing_points: List[Vertex]) -> None:
        """
        Draw the complete Delaunay triangulation.
        
        Args:
            drawing_points: List of vertices to draw
        """
        for vert in drawing_points:
            for edge in self.get_neighbours(vert):
                self.turtle.penup()
                self.turtle.goto(edge.V.getxy()[0] + 15, edge.V.getxy()[1])
                self.turtle.write(edge.V.Vertex_id)
                self.turtle.goto(edge.V.getxy())
                self.turtle.pendown()
                self.turtle.goto(edge.Sym().V.getxy())
                self.turtle.penup()
                self.turtle.goto(edge.Sym().V.getxy()[0] + 15, edge.Sym().V.getxy()[1])
                self.turtle.write(edge.Sym().V.Vertex_id)

    def draw_line(self, edge: HalfEdge, color: str = "brown", width: int = 5) -> None:
        """
        Draw a line between two vertices.
        
        Args:
            edge: The half-edge to draw
            color: Color of the line
            width: Width of the line
        """
        self.turtle.penup()
        self.turtle.pensize(width)
        self.turtle.pencolor(color)
        self.turtle.goto(edge.V.getxy())
        self.turtle.pendown()
        self.turtle.goto(edge.S.V.getxy())
        self.turtle.penup()
        self.turtle.pensize(1)

    def delete_line(self) -> None:
        """Delete the currently drawn line."""
        if self.taken_edge:
            self.draw_line(self.taken_edge, "white", 5)
            self.taken_edge = None

    def next_edge(self) -> None:
        """Move to the next edge in the triangulation."""
        self.turtle.setheading(90)
        self.turtle.forward(100)

    def prev_edge(self) -> None:
        """Move to the previous edge in the triangulation."""
        pass  # To be implemented

    def sym_edge(self) -> None:
        """Move to the symmetric edge."""
        pass  # To be implemented

    def exit_screen(self) -> None:
        """Exit the turtle graphics window."""
        turtle.bye()

    def click_on_edge(self, x: float, y: float) -> None:
        """
        Handle mouse click events to select edges.
        
        Args:
            x: X coordinate of the click
            y: Y coordinate of the click
        """
        point = Vertex(x, y)
        if self.main_edge:
            searching_tri = self.walk_in_tri(self.main_edge, point)
            self.drawing_edge = self.distance_from(searching_tri, point)
            self.draw_selected_edge()

    def add_point(self, x: float, y: float) -> None:
        """
        Add a new point to the triangulation.
        
        Args:
            x: X coordinate of the new point
            y: Y coordinate of the new point
        """
        pass  # To be implemented

    def distance_from(self, edges: List[HalfEdge], point: Vertex) -> HalfEdge:
        """
        Calculate the distance from a point to the nearest edge.
        
        Args:
            edges: List of edges to check
            point: Point to calculate distance from
            
        Returns:
            The nearest edge to the point
        """
        if not edges:
            return None
            
        min_dist = float('inf')
        nearest_edge = None
        
        for edge in edges:
            mid_x = (edge.V.getxy()[0] + edge.S.V.getxy()[0]) / 2
            mid_y = (edge.V.getxy()[1] + edge.S.V.getxy()[1]) / 2
            dist = math.sqrt((mid_x - point.getxy()[0])**2 + (mid_y - point.getxy()[1])**2)
            
            if dist < min_dist:
                min_dist = dist
                nearest_edge = edge
                
        return nearest_edge

    def walk_in_tri(self, edge: HalfEdge, point: Vertex) -> List[HalfEdge]:
        """
        Walk through the triangulation to find the triangle containing the point.
        
        Args:
            edge: Starting edge
            point: Point to locate
            
        Returns:
            List of edges forming the containing triangle
        """
        # Implementation to be added
        pass

    def get_neighbours(self, vertex: Vertex) -> List[HalfEdge]:
        """
        Get all neighboring edges of a vertex.
        
        Args:
            vertex: Vertex to get neighbors for
            
        Returns:
            List of neighboring edges
        """
        # Implementation to be added
        pass

    def draw_selected_edge(self) -> None:
        """Draw the currently selected edge."""
        if self.taken_edge:
            self.delete_line()
        self.taken_edge = self.drawing_edge
        self.drawing_edge = None
        if self.taken_edge:
            self.draw_line(self.taken_edge, "brown", 5)

    def run(self, initial_edge: HalfEdge, drawing_points: List[Vertex]) -> None:
        """
        Start the visualization.
        
        Args:
            initial_edge: Starting edge for the visualization
            drawing_points: List of vertices to draw
        """
        self.main_edge = initial_edge
        self.draw_delaunay_triangulation(drawing_points)
        turtle.mainloop() 