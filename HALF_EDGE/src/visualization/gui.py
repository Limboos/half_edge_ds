"""
GUI-based visualization module for Half-Edge data structures.
Provides interactive visualization capabilities using PyQt.
"""
from typing import List, Optional, Tuple
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QSpinBox,
                            QComboBox, QMessageBox, QToolBar, QStatusBar)
from PyQt6.QtCore import Qt, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QAction, QIcon
import logging
import random

from ..core.half_edge_ds import HalfEdge, Vertex
from ..algorithms.delaunay import DelaunayTriangulation

logger = logging.getLogger(__name__)

class HalfEdgeCanvas(QWidget):
    """A widget for drawing Half-Edge data structures."""
    
    vertex_added = pyqtSignal(Vertex)
    edge_selected = pyqtSignal(HalfEdge)
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the canvas."""
        super().__init__(parent)
        self.vertices: List[Vertex] = []
        self.edges: List[HalfEdge] = []
        self.selected_edge: Optional[HalfEdge] = None
        self.selected_vertex: Optional[Vertex] = None
        self.drawing_mode: str = "vertex"  # "vertex" or "edge"
        self.setMinimumSize(800, 600)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: white;")

    def set_data(self, vertices: List[Vertex], edges: List[HalfEdge]) -> None:
        """Set the data to be visualized."""
        logger.debug(f"[HalfEdgeCanvas] Received {len(vertices)} vertices and {len(edges)} edges")
        self.vertices = vertices
        self.edges = edges
        self.update()

    def paintEvent(self, event) -> None:
        """Handle paint events."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw edges
        for edge in self.edges:
            start = edge.V.getxy()
            end = edge.S.V.getxy()
            
            # Set pen style based on edge type
            if edge == self.selected_edge:
                pen = QPen(QColor(255, 0, 0))  # Red for selected edge
                pen.setWidth(3)
            else:
                pen = QPen(QColor(0, 0, 255))  # Blue for normal edges
                pen.setWidth(2)
            
            painter.setPen(pen)
            painter.drawLine(
                int(start[0]), int(start[1]),
                int(end[0]), int(end[1])
            )

        # Draw vertices
        for vertex in self.vertices:
            pos = vertex.getxy()
            
            # Set brush color based on selection
            if vertex == self.selected_vertex:
                painter.setBrush(QColor(255, 0, 0))  # Red for selected vertex
            else:
                painter.setBrush(QColor(255, 255, 255))  # White for normal vertices
            
            # Draw vertex circle
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.drawEllipse(QPointF(pos[0], pos[1]), 5, 5)
            
            # Draw vertex ID
            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.setFont(QFont('Arial', 10))
            painter.drawText(
                int(pos[0] + 10),
                int(pos[1] - 10),
                str(vertex.Vertex_id)
            )

    def mousePressEvent(self, event) -> None:
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            pos = (event.position().x(), event.position().y())
            
            if self.drawing_mode == "vertex":
                # Add new vertex
                vertex = Vertex(pos[0], pos[1])
                self.vertices.append(vertex)
                self.vertex_added.emit(vertex)
                self.update()
            else:
                # Select nearest edge
                self.select_nearest_edge(pos)

    def select_nearest_edge(self, point: Tuple[float, float]) -> None:
        """Select the edge nearest to the given point."""
        min_dist = float('inf')
        nearest_edge = None
        
        for edge in self.edges:
            start = edge.V.getxy()
            end = edge.S.V.getxy()
            dist = self.point_to_line_distance(point, start, end)
            
            if dist < min_dist:
                min_dist = dist
                nearest_edge = edge
        
        if min_dist < 10:  # Threshold for selection
            self.selected_edge = nearest_edge
            self.edge_selected.emit(nearest_edge)
            self.update()

    def point_to_line_distance(self, point: Tuple[float, float],
                             line_start: Tuple[float, float],
                             line_end: Tuple[float, float]) -> float:
        """Calculate the distance from a point to a line segment."""
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        A = x - x1
        B = y - y1
        C = x2 - x1
        D = y2 - y1

        dot = A * C + B * D
        len_sq = C * C + D * D

        if len_sq == 0:
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5

        param = dot / len_sq

        if param < 0:
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
        elif param > 1:
            return ((x - x2) ** 2 + (y - y2) ** 2) ** 0.5
        else:
            x_proj = x1 + param * C
            y_proj = y1 + param * D
            return ((x - x_proj) ** 2 + (y - y_proj) ** 2) ** 0.5

    def set_drawing_mode(self, mode: str) -> None:
        """Set the current drawing mode."""
        self.drawing_mode = mode

class MainWindow(QMainWindow):
    """Main window for the Half-Edge visualization application."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle("Half-Edge Structure Visualizer")
        self.setMinimumSize(1200, 800)
        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the user interface."""
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create canvas
        self.canvas = HalfEdgeCanvas()
        layout.addWidget(self.canvas, stretch=1)

        # Create control panel
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_panel.setMaximumWidth(300)
        layout.addWidget(control_panel)

        # Add mode selection
        mode_label = QLabel("Drawing Mode:")
        control_layout.addWidget(mode_label)
        
        mode_combo = QComboBox()
        mode_combo.addItems(["Add Vertex", "Select Edge"])
        mode_combo.currentTextChanged.connect(self.change_mode)
        control_layout.addWidget(mode_combo)

        # Add buttons
        add_random_btn = QPushButton("Add Random Vertex")
        add_random_btn.clicked.connect(self.add_random_vertex)
        control_layout.addWidget(add_random_btn)

        triangulate_btn = QPushButton("Perform Triangulation")
        triangulate_btn.clicked.connect(self.perform_triangulation)
        control_layout.addWidget(triangulate_btn)

        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        control_layout.addWidget(clear_btn)

        # Add status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")

        # Connect signals
        self.canvas.vertex_added.connect(self.on_vertex_added)
        self.canvas.edge_selected.connect(self.on_edge_selected)

    def change_mode(self, mode: str) -> None:
        """Change the drawing mode."""
        self.canvas.set_drawing_mode("vertex" if mode == "Add Vertex" else "edge")
        self.statusBar.showMessage(f"Mode: {mode}")

    def add_random_vertex(self) -> None:
        """Add a random vertex to the canvas."""
        x = random.randint(50, self.canvas.width() - 50)
        y = random.randint(50, self.canvas.height() - 50)
        vertex = Vertex(x, y)
        self.canvas.vertices.append(vertex)
        self.canvas.update()
        self.statusBar.showMessage(f"Added vertex {vertex.Vertex_id} at ({x}, {y})")

    def perform_triangulation(self) -> None:
        """Perform Delaunay triangulation on the current vertices."""
        if len(self.canvas.vertices) < 3:
            QMessageBox.warning(self, "Warning", "Need at least 3 vertices for triangulation")
            return

        try:
            # Create Delaunay triangulation
            delaunay = DelaunayTriangulation(self.canvas.vertices)
            new_edges = delaunay.triangulate()
            
            # Update canvas
            self.canvas.edges = new_edges
            self.canvas.update()
            self.statusBar.showMessage(f"Triangulation completed with {len(new_edges)} edges")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Triangulation failed: {str(e)}")

    def clear_all(self) -> None:
        """Clear all vertices and edges."""
        self.canvas.vertices.clear()
        self.canvas.edges.clear()
        self.canvas.selected_edge = None
        self.canvas.selected_vertex = None
        self.canvas.update()
        self.statusBar.showMessage("Cleared all data")

    def on_vertex_added(self, vertex: Vertex) -> None:
        """Handle vertex addition."""
        self.statusBar.showMessage(f"Added vertex {vertex.Vertex_id}")

    def on_edge_selected(self, edge: HalfEdge) -> None:
        """Handle edge selection."""
        self.statusBar.showMessage(
            f"Selected edge {edge.id}: {edge.V.Vertex_id} -> {edge.S.V.Vertex_id}"
        )

def run_visualization(vertices: List[Vertex], edges: List[HalfEdge]) -> None:
    """Run the visualization application."""
    app = QApplication([])
    window = MainWindow()
    window.canvas.set_data(vertices, edges)
    window.show()
    app.exec() 