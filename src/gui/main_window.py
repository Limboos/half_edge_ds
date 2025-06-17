import tkinter as tk
from tkinter import ttk
import logging
from typing import List, Optional
from ..core.half_edge import HalfEdge, Vertex, Face, Fast_splice, verify_connectivity
from ..algorithms.delaunay import DelaunayTriangulation

logger = logging.getLogger(__name__)

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Half-Edge Structure Viewer")
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create canvas for drawing
        self.canvas = tk.Canvas(self.main_frame, width=800, height=600, bg='white')
        self.canvas.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create buttons frame
        self.button_frame = ttk.Frame(self.main_frame, padding="5")
        self.button_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Add buttons
        self.add_vertex_btn = ttk.Button(self.button_frame, text="Add Vertex", command=self.add_vertex)
        self.add_vertex_btn.grid(row=0, column=0, padx=5)
        
        self.connect_edges_btn = ttk.Button(self.button_frame, text="Connect Edges", command=self.connect_edges)
        self.connect_edges_btn.grid(row=0, column=1, padx=5)
        
        self.create_face_btn = ttk.Button(self.button_frame, text="Create Face", command=self.create_face)
        self.create_face_btn.grid(row=0, column=2, padx=5)
        
        self.delaunay_btn = ttk.Button(self.button_frame, text="Delaunay Triangulation", command=self.perform_delaunay)
        self.delaunay_btn.grid(row=0, column=3, padx=5)
        
        # Initialize data structures
        self.vertices: List[Vertex] = []
        self.edges: List[HalfEdge] = []
        self.faces: List[Face] = []
        
        # Bind canvas click event
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        x, y = event.x, event.y
        logger.debug(f"Canvas clicked at ({x}, {y})")
        self.add_vertex_at(x, y)
        
    def add_vertex_at(self, x: float, y: float):
        """Add a new vertex at the specified coordinates"""
        vertex = Vertex(x, y)
        self.vertices.append(vertex)
        logger.info(f"Added vertex {vertex.id} at ({x}, {y})")
        self.draw_vertex(vertex)
        
    def draw_vertex(self, vertex: Vertex):
        """Draw a vertex on the canvas"""
        x, y = vertex.x, vertex.y
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill='black')
        self.canvas.create_text(x+10, y+10, text=str(vertex.id))
        
    def add_vertex(self):
        """Add a vertex at a random position"""
        import random
        x = random.randint(50, 750)
        y = random.randint(50, 550)
        self.add_vertex_at(x, y)
        
    def connect_edges(self):
        """Connect selected vertices with edges"""
        if len(self.vertices) < 2:
            logger.warning("Need at least 2 vertices to create edges")
            return
            
        # Create edges between consecutive vertices
        for i in range(len(self.vertices)-1):
            edge = HalfEdge(self.vertices[i])
            twin = HalfEdge(self.vertices[i+1])
            edge.twin = twin
            twin.twin = edge
            self.edges.extend([edge, twin])
            logger.info(f"Created edge pair {edge.id} <-> {twin.id}")
            
        # Connect edges using Fast_splice
        try:
            Fast_splice(self.edges)
            if verify_connectivity(self.edges):
                logger.info("Edge connectivity verified successfully")
                self.draw_edges()
            else:
                logger.error("Edge connectivity verification failed")
        except Exception as e:
            logger.error(f"Error in Fast_splice: {str(e)}")
            
    def draw_edges(self):
        """Draw all edges on the canvas"""
        for edge in self.edges:
            start = edge.vertex
            end = edge.next.vertex if edge.next else edge.twin.vertex
            self.canvas.create_line(start.x, start.y, end.x, end.y, fill='blue')
            
    def create_face(self):
        """Create a face from the current edge structure"""
        if not self.edges:
            logger.warning("No edges available to create face")
            return
            
        try:
            face = Face()
            face.edge = self.edges[0]
            for edge in self.edges:
                edge.face = face
            self.faces.append(face)
            logger.info(f"Created face {face.id}")
        except Exception as e:
            logger.error(f"Error creating face: {str(e)}")
            
    def perform_delaunay(self):
        """Perform Delaunay triangulation on the current vertices"""
        if len(self.vertices) < 3:
            logger.warning("Need at least 3 vertices for Delaunay triangulation")
            return
            
        try:
            # Create Delaunay triangulation
            delaunay = DelaunayTriangulation(self.vertices)
            new_edges = delaunay.triangulate()
            
            # Clear existing edges and faces
            self.edges.clear()
            self.faces.clear()
            
            # Add new edges
            self.edges.extend(new_edges)
            
            # Connect edges using Fast_splice
            Fast_splice(self.edges)
            
            # Verify connectivity
            if verify_connectivity(self.edges):
                logger.info("Delaunay triangulation completed successfully")
                self.canvas.delete("all")  # Clear canvas
                for vertex in self.vertices:
                    self.draw_vertex(vertex)
                self.draw_edges()
            else:
                logger.error("Delaunay triangulation connectivity verification failed")
        except Exception as e:
            logger.error(f"Error in Delaunay triangulation: {str(e)}")
            
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run the main window
    app = MainWindow()
    app.run() 