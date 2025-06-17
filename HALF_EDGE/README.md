# Half-Edge Data Structure Implementation

This project implements a half-edge data structure for representing and manipulating polygonal meshes, with a focus on Delaunay triangulation and visualization.

## Project Structure

```
HALF_EDGE/
├── src/
│   ├── core/           # Core data structures (use only these for new code)
│   │   ├── half_edge_ds.py        # Main half-edge implementation (Vertex, HalfEdge, MakeEdge, Splice, etc.)
│   │   ├── half_edge_builder.py   # Builder pattern for half-edges
│   │   └── __init__.py
│   │
│   ├── algorithms/     # Geometric algorithms
│   │   ├── delaunay.py        # Delaunay triangulation
│   │   ├── pathfinding.py     # Path finding algorithms
│   │   └── convex_hull.py     # Convex hull computation
│   │
│   ├── visualization/ # Visualization tools
│   │   ├── gui.py            # Modern GUI (PyQt6)
│   │   ├── main.py           # Main visualization entry point
│   │   ├── turtle_visualizer.py # Turtle-based visualization
│   │   └── __init__.py
│   │
│   └── utils/         # Utility functions
│       ├── database.py       # Database operations
│       └── data_io.py        # Data input/output
│
│   └── legacy/        # Old/duplicate/legacy code (do not use in new code)
│       ├── half_edge.py
│       ├── edge.py
│       ├── validation.py
│       ├── face.py
│       ├── vertex.py
│       ├── cevent.py
│       ├── old_gui.py
│       └── old_turtle.py
│
├── tests/             # Unit tests
├── examples/          # Example usage
├── docs/              # Documentation
└── data/              # Data files
```

## Core Components (use only these in new code)
- `src/core/half_edge_ds.py`: Główna implementacja struktur (Vertex, HalfEdge, MakeEdge, Splice, neighbours, ...)
- `src/core/half_edge_builder.py`: Builder do wygodnego tworzenia grafów

## Usage

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the visualization:**
```bash
python -m src.visualization.main --file data/graph.obj
```

3. **File format:**
- Vertices: `v x.y` (e.g. `v 1.55` means x=1, y=55)
- Faces: `f 1 2 3` (indices start at 1)

4. **Basic imports for your code:**
```python
from src.core.half_edge_ds import Vertex, HalfEdge, MakeEdge, Splice
from src.core.half_edge_builder import HalfEdgeBuilder
```

## Key Features
- Half-Edge operations: splicing, splitting, face creation, connectivity verification
- Delaunay triangulation, convex hull, pathfinding
- Modern GUI (PyQt6) and turtle-based visualization
- Clean, maintainable, PEP8-compliant code
- All legacy/duplicate code is in `src/legacy/` (do not use in new code)

## Development
- Add new features only to `src/core/half_edge_ds.py` and `src/core/half_edge_builder.py`
- Use only these modules in algorithms, visualization, and tests
- All imports should point to these files
- Run tests with:
```bash
python -m pytest tests/
```

## License
MIT License 