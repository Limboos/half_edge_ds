from HALF_EDGE.Turtle_drawing import *
from HALF_EDGE.half_edge import *
import numpy as np
from scipy.spatial import Delaunay
import pandas as pd
import matplotlib.pyplot as plt
import turtle
import tkinter
import logging
from typing import List, Tuple, Optional
from ..core.half_edge import HalfEdge, Vertex, Face, Fast_splice, verify_connectivity

logger = logging.getLogger(__name__)

# TODO


class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)


def BigTri(v):
    tri = []
    e = []
    x = v.getxy()[0]
    y = v.getxy()[1]
    tri.append(Vertex(x - 5000, y - 5000))
    tri.append(Vertex(x + 5000, y - 5000))
    tri.append(Vertex((x + x) / 2, y + 5000))
    e.append(MakeEdge(tri[0], tri[1]))
    e.append(MakeEdge(tri[1], tri[2]))
    e.append(MakeEdge(tri[2], tri[0]))
    Splice(e[0], e[2].Sym())
    Splice(e[1], e[0].Sym())
    Splice(e[2], e[1].Sym())
    return e


def Circlecenter(tri):
    pts = np.asarray([v.getxy() for v in tri])
    pts2 = np.dot(pts, pts.T)
    A = np.bmat([[2 * pts2, [[1],
                             [1],
                             [1]]],
                 [[[1, 1, 1, 0]]]])

    b = np.hstack((np.sum(pts * pts, axis=1), [1]))
    x = np.linalg.solve(A, b)
    bary_coords = x[:-1]
    center = np.dot(bary_coords, pts)
    center[0] = round(center[0], 0)
    center[1] = round(center[1], 0)
    radius = np.sum(np.square(pts[0] - center))  # squared distance
    return (center, radius)


def ExportData(v):
    x_cordinate = []
    y_cordinate = []
    x_cordinate.append(i.getxy()[0])
    y_cordinate.append(i.getxy()[1])
    return x_cordinate, y_cordinate


def Quicksort(l):
    if len(l) <= 1: return l
    pivolt = l[random.randint(0, len(l) - 1)]
    small, eq, larger = [], [], []
    for i in l:
        dis = i
        if dis < pivolt:
            small.append(i)
        elif dis == pivolt:
            eq.append(i)
        else:
            larger.append(i)
    return Quicksort(small) + eq + Quicksort(larger)


def InCircleFast(tri, p):
    """Check if point p is inside of precomputed circumcircle of tri.
    """
    center, radius = Circlecenter(tri)
    return np.sum(np.square(center - p.getxy())) <= radius


def RemoveSplice(t1, t2, t3):
    Splice(t1, t2)
    Splice(t3.Sym(), t2.Sym())
    Splice(t1.Sym(), t2)


def NewEdges(x, p):
    e = []
    e.append(MakeEdge(x.V, p))
    e.append(MakeEdge(x.NextV().Sym().V, p))
    e.append(MakeEdge(x.N.S.N.S.V, p))
    return e


def Newconection(x, e):
    temp = x.NextV()
    Splice(x, temp)
    Splice(x, e)
    Splice(e, temp)


def SplitingTheTri(x, p):
    e = NewEdges(x, p)
    t = x.N.S
    t1 = x.N.S.N.S
    '''
    print("=-----")
    print("MAIN EDGE: ", x.V.Vertex_id, x.S.V.Vertex_id)
    print("SPLITING THE TRIANGLE")

    print(x.V.Vertex_id, x.S.V.Vertex_id, "||", e[0].V.Vertex_id, e[0].S.V.Vertex_id)
    print(t1.V.Vertex_id, t1.S.V.Vertex_id, "||", e[2].V.Vertex_id, e[2].S.V.Vertex_id)
    print(t.V.Vertex_id, t.S.V.Vertex_id, "||", e[1].V.Vertex_id, e[1].S.V.Vertex_id)
    print(e[1].S.V.Vertex_id, e[1].S.S.V.Vertex_id, "||", e[0].S.V.Vertex_id, e[0].S.S.V.Vertex_id)
    print(e[2].S.V.Vertex_id, e[0].S.S.V.Vertex_id, "||", e[2].S.V.Vertex_id, e[2].S.S.V.Vertex_id)
    print("--------")
    '''
    Newconection(x, e[0])
    Newconection(t1, e[2])
    Newconection(t, e[1])
    Splice(e[1].S, e[0].S)
    Splice(e[0].S, e[2].S)
    return e


def Flip(x, p):
    for i in neighbours(x):
        if i.V.Vertex_id == p.Vertex_id:
            temp = x.N
            temp1 = x.N.S.N.S
            temp2 = x.S.N
            temp3 = x.S.N.S.N.S
            Splice(temp3, x)
            # Splice(x, temp)
            Splice(temp.S, temp1.S)
            Splice(temp1, x.S)
            # Splice(x.S, temp2)
            Splice(temp2.S, temp3.S)
            del x

            e = MakeEdge(temp.S.V, temp3.S.V)
            Splice(temp2.S, e.S)
            Splice(e.S, temp3.S)
            Splice(temp.S, e)
            Splice(e, temp1.S)

            return e, temp2.S, temp3
        else:
            pass


def R(p, p1, p2):
    px = p.getxy()[0]
    py = p.getxy()[1]
    p1x = p1.V.getxy()[0]
    p1y = p1.V.getxy()[1]
    p2x = p2.V.getxy()[0]
    p2y = p2.V.getxy()[1]
    x = np.linalg.det([[px, py, 1],
                       [p1x, p1y, 1],
                       [p2x, p2y, 1]])
    return x


def CCW(p, p1, p2):
    px = p.V.getxy()[0]
    py = p.V.getxy()[1]
    p1x = p1.V.getxy()[0]
    p1y = p1.V.getxy()[1]
    p2x = p2.V.getxy()[0]
    p2y = p2.V.getxy()[1]
    x = np.linalg.det([[px, py, 1],
                       [p1x, p1y, 1],
                       [p2x, p2y, 1]])
    return x


def Point_inside_tri(e, p):
    if int(R(p, e.S, e.N.S)) >= 0 and int(R(p, e.N.S, e)) >= 0 and int(R(p, e, e.S)) >= 0:
        return e
    else:
        return e.S


def WalkingInTri(e, p, con):
    while True:
        if int(R(p, e.S, e.N.S)) >= 0 and int(R(p, e.N.S, e)) >= 0 and int(R(p, e, e.S)) >= 0:
            if p.Vertex_id >= 2 and e.N.S.V.getxy() in con and e.V.getxy() in con and e.S.V.getxy() in con:
                e = e.N
            else:
                return e.N.S, e, e.N.S.N.S
        elif int(R(p, e.S, e.N.S)) <= 0 and int(R(p, e.N.S, e)) <= 0 and int(R(p, e, e.S)) <= 0:
            e = e.S
        elif R(p, e.S, e.N.S) < 0:
            e = e.N.S.N
        elif R(p, e.N.S, e) < 0:
            e = e.N
        elif R(p, e, e.S) < 0:
            e = e.S


def Delauny(point, edge):
    # print(" VERTEX NR:", point.Vertex_id)
    bad_triangles = WalkingInTri(edge[-1], point, tri)
    stack = Stack()
    for i in bad_triangles:
        stack.push(i)
    del edge
    edge = []
    s = SplitingTheTri(bad_triangles[0], point)
    for k in s:
        edge.append(k)
    while stack.size() != 0:
        temp = stack.pop()
        # print(temp.V.Vertex_id, temp.S.V.Vertex_id)
        # print(temp.V.Vertex_id, point.Vertex_id, temp.Sym().V.Vertex_id,
        # Point_inside_tri(temp, point).S.N.S.V.Vertex_id)
        if InCircleFast([temp.V, point, temp.Sym().V], Point_inside_tri(temp, point).S.N.S.V):
            f = Flip(temp, point)
            # print("PUSH")
            # print(f[1].V.Vertex_id, f[1].S.V.Vertex_id)
            # print(f[2].V.Vertex_id, f[2].S.V.Vertex_id)
            del temp

            stack.push(f[1])
            stack.push(f[2])
            edge.append(f[0])

        else:
            pass
    return edge


def ReturnVertex(v):
    return v


def DrawDT(drawing_points):
    t._tracer(0)
    # Function for drawing the whole DT
    for vert in drawing_points:
        for i in neighbours(vert):
            logger.debug(f"DrawDT: Drawing edge from {i.V.Vertex_id} to {i.S.V.Vertex_id}")
            turtle.penup()
            turtle.goto(i.V.getxy()[0] + 15, i.V.getxy()[1])
            turtle.write(i.V.Vertex_id)
            turtle.goto(i.V.getxy())
            turtle.pendown()
            turtle.goto(i.Sym().V.getxy())
            turtle.penup()
            turtle.goto(i.Sym().V.getxy()[0] + 15, i.Sym().V.getxy()[1])
            turtle.write(i.Sym().V.Vertex_id)


def DeletingLine():
    global drawing_edge
    global taken_edge
    Turtle_drawingline(taken_edge, "white", 5)
    Turtle_drawingline(taken_edge, "black", 1)
    taken_edge = None


def Turtle_drawingline(edge, color, width):
    t.penup()
    t.pensize(width)
    t.pencolor(color)
    t.goto(edge.V.getxy())
    t.pendown()
    t.goto(edge.S.V.getxy())
    t.penup()
    t.pensize(1)


def DrawingLine():
    global drawing_edge
    global taken_edge
    if taken_edge != None:
        DeletingLine()
    taken_edge = drawing_edge
    drawing_edge = None
    Turtle_drawingline(taken_edge, "brown", 5)


def NextEdge():
    global taken_edge
    global drawing_edge
    if taken_edge == None:
        pass
    drawing_edge = taken_edge.N
    DrawingLine()


def PrevEdge():
    global taken_edge
    global drawing_edge
    if taken_edge == None:
        pass
    drawing_edge = taken_edge.S.N.S.N.S
    DrawingLine()


def SymEdge():
    global taken_edge
    global drawing_edge
    if taken_edge == None:
        pass
    drawing_edge =taken_edge.S
    DrawingLine()
def ExitScrean():
    turtle.bye()


def distance(point, coef):
    return abs((coef[0] * point[0]) - point[1] + coef[1]) / math.sqrt((coef[0] * coef[0]) + 1)


def DistanceFrom(e, point):
    distance = np.linalg.norm(np.cross(np.array(e[0].S.V.getxy()) - np.array(e[0].V.getxy()),
                                       np.array(e[0].V.getxy()) - np.array(point.getxy()))) / np.linalg.norm(
        np.array(e[0].S.V.getxy()) - np.array(e[0].V.getxy()))
    distance1 = np.linalg.norm(np.cross(np.array(e[1].S.V.getxy()) - np.array(e[1].V.getxy()),
                                        np.array(e[1].V.getxy()) - np.array(point.getxy()))) / np.linalg.norm(
        np.array(e[1].S.V.getxy()) - np.array(e[1].V.getxy()))
    distance2 = np.linalg.norm(np.cross(np.array(e[2].S.V.getxy()) - np.array(e[2].V.getxy()),
                                        np.array(e[2].V.getxy()) - np.array(point.getxy()))) / np.linalg.norm(
        np.array(e[2].S.V.getxy()) - np.array(e[2].V.getxy()))

    if distance < distance1 and distance < distance2:
        return e[0]
    elif distance1 < distance and distance1 < distance2:
        return e[1]
    elif distance2 < distance1 and distance2 < distance:
        return e[2]


def ClickOnEdge(x, y):
    # Findning the nearest line to the position where you click
    global drawing_edge
    global taken_edge
    global main_edge
    point = Vertex(x, y)
    if taken_edge != None:
        turtle.resetscreen()
        remove_teken(edges)
        remove_visited(vertex)
        drawing_points = bfs(taken_edge)
        DrawDT(drawing_points)
        taken_edge = None
    searching_tri = WalkingInTri(main_edge, point, tri)
    drawing_edge = DistanceFrom(searching_tri, point)
    DrawingLine()



def AddPoint(x, y):
    global edges
    global vertex
    global taken_edge
    vertex.append(Vertex(x, y))

    et = Delauny(vertex[-1], edges)
    for ez in et:
        edges.append(ez)
    turtle.resetscreen()
    remove_teken(edges)
    remove_visited(vertex)
    drawing_points = bfs(edges[-1])
    DrawDT(drawing_points)
    # NIE DZIAŁA DODAWANIE PUNKTU, COS NIE TAK Z bfs


class DelaunayTriangulation:
    def __init__(self, vertices: List[Vertex]):
        """
        Initialize Delaunay triangulation with a list of vertices.
        
        Args:
            vertices: List of vertices to triangulate
        """
        self.vertices = vertices
        self.edges: List[HalfEdge] = []
        self.faces: List[Face] = []
        
    def _create_super_triangle(self) -> Tuple[Vertex, Vertex, Vertex]:
        """
        Create a super triangle that contains all vertices.
        
        Returns:
            Tuple of three vertices forming the super triangle
        """
        # Find bounding box
        x_coords = [v.x for v in self.vertices]
        y_coords = [v.y for v in self.vertices]
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)
        
        # Add padding
        padding = max(max_x - min_x, max_y - min_y) * 0.5
        
        # Create super triangle vertices
        v1 = Vertex(min_x - padding, min_y - padding)
        v2 = Vertex(max_x + padding, min_y - padding)
        v3 = Vertex((min_x + max_x) / 2, max_y + padding)
        
        logger.debug(f"Created super triangle with vertices: {v1.id}, {v2.id}, {v3.id}")
        return v1, v2, v3
        
    def _is_delaunay(self, edge: HalfEdge) -> bool:
        """
        Check if an edge satisfies the Delaunay condition.
        
        Args:
            edge: Half-edge to check
            
        Returns:
            bool: True if the edge satisfies Delaunay condition
        """
        if not edge.twin or not edge.twin.face:
            return True
            
        # Get the four vertices of the two adjacent triangles
        v1 = edge.vertex
        v2 = edge.next.vertex
        v3 = edge.next.next.vertex
        v4 = edge.twin.next.next.vertex
        
        # Check if v4 is inside the circumcircle of triangle v1,v2,v3
        return not self._in_circumcircle(v1, v2, v3, v4)
        
    def _in_circumcircle(self, v1: Vertex, v2: Vertex, v3: Vertex, v4: Vertex) -> bool:
        """
        Check if vertex v4 is inside the circumcircle of triangle v1,v2,v3.
        
        Args:
            v1, v2, v3: Vertices of the triangle
            v4: Vertex to check
            
        Returns:
            bool: True if v4 is inside the circumcircle
        """
        # Convert to numpy arrays for easier computation
        p1 = np.array([v1.x, v1.y])
        p2 = np.array([v2.x, v2.y])
        p3 = np.array([v3.x, v3.y])
        p4 = np.array([v4.x, v4.y])
        
        # Compute circumcircle center and radius
        d = 2 * (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))
        if abs(d) < 1e-10:
            return False
            
        ux = ((p1[0]**2 + p1[1]**2) * (p2[1] - p3[1]) +
              (p2[0]**2 + p2[1]**2) * (p3[1] - p1[1]) +
              (p3[0]**2 + p3[1]**2) * (p1[1] - p2[1])) / d
              
        uy = ((p1[0]**2 + p1[1]**2) * (p3[0] - p2[0]) +
              (p2[0]**2 + p2[1]**2) * (p1[0] - p3[0]) +
              (p3[0]**2 + p3[1]**2) * (p2[0] - p1[0])) / d
              
        center = np.array([ux, uy])
        radius = np.linalg.norm(p1 - center)
        
        # Check if v4 is inside the circumcircle
        return np.linalg.norm(p4 - center) < radius
        
    def _flip_edge(self, edge: HalfEdge) -> None:
        """
        Flip an edge to maintain Delaunay condition.
        
        Args:
            edge: Half-edge to flip
        """
        if not edge.twin or not edge.twin.face:
            return
            
        # Get the four vertices
        v1 = edge.vertex
        v2 = edge.next.vertex
        v3 = edge.next.next.vertex
        v4 = edge.twin.next.next.vertex
        
        # Create new edges
        new_edge = HalfEdge(v1)
        new_twin = HalfEdge(v3)
        new_edge.twin = new_twin
        new_twin.twin = new_edge
        
        # Update next pointers
        new_edge.next = edge.next.next
        new_twin.next = edge.twin.next.next
        edge.next.next.next = new_twin
        edge.twin.next.next.next = new_edge
        
        # Update face pointers
        face1 = Face()
        face2 = Face()
        face1.edge = new_edge
        face2.edge = new_twin
        
        # Update edge-face relationships
        new_edge.face = face1
        new_twin.face = face2
        edge.next.next.face = face1
        edge.twin.next.next.face = face2
        
        # Add new faces
        self.faces.extend([face1, face2])
        
        logger.debug(f"Flipped edge {edge.id} <-> {edge.twin.id} to {new_edge.id} <-> {new_twin.id}")
        
    def triangulate(self) -> List[HalfEdge]:
        """
        Perform Delaunay triangulation on the vertices.
        
        Returns:
            List of half-edges forming the triangulation
        """
        if len(self.vertices) < 3:
            logger.warning("Need at least 3 vertices for triangulation")
            return []
            
        # Create super triangle
        v1, v2, v3 = self._create_super_triangle()
        
        # Create initial triangle
        e1 = HalfEdge(v1)
        e2 = HalfEdge(v2)
        e3 = HalfEdge(v3)
        
        e1.next = e2
        e2.next = e3
        e3.next = e1
        
        face = Face()
        face.edge = e1
        e1.face = face
        e2.face = face
        e3.face = face
        
        self.edges.extend([e1, e2, e3])
        self.faces.append(face)
        
        # Insert each vertex
        for vertex in self.vertices:
            self._insert_vertex(vertex)
            
        # Remove super triangle edges
        self._remove_super_triangle(v1, v2, v3)
        
        # Verify connectivity
        if not verify_connectivity(self.edges):
            logger.error("Triangulation connectivity verification failed")
            return []
            
        logger.info(f"Completed Delaunay triangulation with {len(self.edges)} edges and {len(self.faces)} faces")
        return self.edges
        
    def _insert_vertex(self, vertex: Vertex) -> None:
        """
        Insert a vertex into the triangulation.
        
        Args:
            vertex: Vertex to insert
        """
        # Find the triangle containing the vertex
        containing_edge = self._find_containing_edge(vertex)
        if not containing_edge:
            logger.error(f"Could not find containing triangle for vertex {vertex.id}")
            return
            
        # Split the triangle
        self._split_triangle(containing_edge, vertex)
        
        # Legalize edges
        self._legalize_edges(vertex)
        
    def _find_containing_edge(self, vertex: Vertex) -> Optional[HalfEdge]:
        """
        Find an edge of the triangle containing the vertex.
        
        Args:
            vertex: Vertex to find containing triangle for
            
        Returns:
            HalfEdge: An edge of the containing triangle, or None if not found
        """
        for edge in self.edges:
            if self._point_in_triangle(vertex, edge):
                return edge
        return None
        
    def _point_in_triangle(self, point: Vertex, edge: HalfEdge) -> bool:
        """
        Check if a point is inside a triangle.
        
        Args:
            point: Point to check
            edge: An edge of the triangle
            
        Returns:
            bool: True if the point is inside the triangle
        """
        v1 = edge.vertex
        v2 = edge.next.vertex
        v3 = edge.next.next.vertex
        
        def sign(p1: Vertex, p2: Vertex, p3: Vertex) -> float:
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
            
        d1 = sign(point, v1, v2)
        d2 = sign(point, v2, v3)
        d3 = sign(point, v3, v1)
        
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        
        return not (has_neg and has_pos)
        
    def _split_triangle(self, edge: HalfEdge, vertex: Vertex) -> None:
        """
        Split a triangle by inserting a vertex.
        
        Args:
            edge: An edge of the triangle to split
            vertex: Vertex to insert
        """
        # Create new edges
        e1 = HalfEdge(vertex)
        e2 = HalfEdge(vertex)
        e3 = HalfEdge(vertex)
        
        # Create new faces
        f1 = Face()
        f2 = Face()
        f3 = Face()
        
        # Update next pointers
        e1.next = edge.next
        e2.next = edge.next.next
        e3.next = edge
        
        edge.next.next.next = e1
        edge.next.next = e2
        edge.next = e3
        
        # Update face pointers
        f1.edge = e1
        f2.edge = e2
        f3.edge = e3
        
        e1.face = f1
        e2.face = f2
        e3.face = f3
        edge.next.next.face = f1
        edge.next.face = f2
        edge.face = f3
        
        # Add new edges and faces
        self.edges.extend([e1, e2, e3])
        self.faces.extend([f1, f2, f3])
        
        logger.debug(f"Split triangle at edge {edge.id} with vertex {vertex.id}")
        
    def _legalize_edges(self, vertex: Vertex) -> None:
        """
        Legalize edges after inserting a vertex.
        
        Args:
            vertex: The inserted vertex
        """
        # Find edges connected to the vertex
        connected_edges = [e for e in self.edges if e.vertex == vertex]
        
        for edge in connected_edges:
            if not self._is_delaunay(edge):
                self._flip_edge(edge)
                
    def _remove_super_triangle(self, v1: Vertex, v2: Vertex, v3: Vertex) -> None:
        """
        Remove edges and faces connected to the super triangle vertices.
        
        Args:
            v1, v2, v3: Vertices of the super triangle
        """
        # Find edges connected to super triangle vertices
        super_edges = [e for e in self.edges if e.vertex in (v1, v2, v3)]
        
        # Remove these edges and their associated faces
        for edge in super_edges:
            if edge in self.edges:
                self.edges.remove(edge)
            if edge.twin in self.edges:
                self.edges.remove(edge.twin)
            if edge.face in self.faces:
                self.faces.remove(edge.face)
            if edge.twin and edge.twin.face in self.faces:
                self.faces.remove(edge.twin.face)
                
        logger.debug("Removed super triangle edges and faces")


if __name__ == '__main__':
    global drawing_edge
    global taken_edge
    global main_edge
    global drawing_points
    global vertex
    global edges
    vertex = []

    #data = pd.read_csv(r'C:\Users\Student240914\Desktop\inzynierka\__Napisane\Programy i dane\Magiczne Bloczki\Dane_wyjatki.csv',sep=";")
    dane=pd.read_csv(r'C:\Users\Student240914\Desktop\inzynierka\__Napisane\Programy i dane\Magiczne Bloczki\Dane_wyjatki.csv',sep=";")
    #
    points = np.array(dane[dane.columns[1:3]])
    for i in points:
         vertex.append(Vertex(i[0]+np.random.rand(1,5)/20,i[1]+np.random.rand(1,7)/10))
    #vertex.append(Vertex(20, 50))
    #vertex.append(Vertex(120, 80))
    #vertex.append(Vertex(100, 220))
    #vertex.append(Vertex(300, 250))
    #vertex.append(Vertex(200, 25))
    # for i in range(100):
    #    vertex.append(Vertex(random.randint(-300, 300), random.randint(-300, 300)))

    edges = []
    global tri
    tri = BigTri(vertex[0])

    for edg in tri:
        edges.append(edg)
    # print(R(vertex[0], edges[0], edges[0].Sym()))
    for element in range(len(tri)):
        tri[element] = tri[element].V.getxy()
    iterr=1
    for j in vertex:
        print(iterr)
        #if iterr==192:
            #break
        et = Delauny(j, edges)
        for ez in et:
            edges.append(ez)
        iterr+=1
    drawing_points = bfs(edges[-1])
    print(drawing_points)
    #turtle.tracer(0)
     #plt.imshow(points)
    #plt.triplot(points[:, 0], points[:, 1])
    #plt.plot(points[:, 0], points[:, 1], 'o')
    #plt.show()


    
    # a=Circlecenter([vertex[0],vertex[1],vertex[2]])
    turtle.tracer(1)
    turtle.tracer(0)
    turtle.done()
    main(vertex)

    #        del edge

    main_edge = edges[0]
    drawing_edge = None
    taken_edge = None
    t = turtle.Turtle()
    t.speed(0)
    DrawDT(drawing_points)

    turtle.onkey(NextEdge, 'w')

    turtle.onkey(PrevEdge, 'e')

    turtle.onkey(SymEdge, 's')

    turtle.onkey(ExitScrean, 'q')

    turtle.onscreenclick(ClickOnEdge, 1)

    turtle.onscreenclick(AddPoint, 3)

    turtle.listen()

    turtle.mainloop()

