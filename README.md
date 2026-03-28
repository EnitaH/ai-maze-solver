#  AI Maze Solver & Visualizer

An interactive pathfinding visualizer built with Python and Pygame, demonstrating how classic algorithms like A* and BFS explore and solve mazes in real time.

---

##  Features

-  A* Search Algorithm
-  Breadth-First Search (BFS)
-  Multiple Heuristics (A*)
  - Manhattan Distance
  - Euclidean Distance
-  Animated Exploration (step-by-step node expansion)
-  Animated Path Reconstruction
-  Interactive Controls
-  Random Solvable Maze Generation
-  Real-time Statistics Panel
-  Pygame-based GUI

---

##  Controls

| Key | Action |
|-----|--------|
| A   | Switch to A* |
| B   | Switch to BFS |
| H   | Toggle heuristic (A* only) |
| R   | Generate new random maze |
| ESC | Exit application |

---

##  Algorithms Overview

### A* Search

An informed search algorithm that uses a heuristic to guide exploration toward the goal efficiently.

f(n) = g(n) + h(n)

- g(n): cost from start to current node  
- h(n): heuristic estimate to goal  

---

### Breadth-First Search (BFS)

An uninformed search algorithm that explores nodes level by level.

- Guarantees shortest path (for unweighted graphs)
- Typically explores more nodes than A*

---

##  Visualization

The visualizer displays:

- 🟩 Start node  
- 🟥 Goal node  
- ⬛ Walls  
- 🟨 Explored nodes  
- 🟦 Final shortest path  

---

##  How to Run

### 1. Install dependencies
```
pip install pygame
```
---

### 2. Run with a predefined maze
```
python visual.py mazes/simple_maze.txt
```
---

### 3. Run with a random maze
```
python visual.py --random 10
```
> The number specifies the maze dimensions (rows × columns).  
> You can increase or decrease it to control the maze size.
>
> Examples:
> - `--random 10` → 10×10 maze  
> - `--random 20` → 20×20 maze
---

## 📁 Project Structure
```
project/
│
├── visual.py
├── main.py
├── requirements.txt
│
├── mazes/
│
└── src/
├── astar.py
├── bfs.py
├── heuristics.py
├── maze.py
├── maze_generator.py
└── node.py
```
---

##  Key Highlights

- Demonstrates informed vs uninformed search
- Shows impact of heuristics in A*
- Interactive learning tool
- Clean and modular code structure

---

##  Future Improvements

- Add Dijkstra’s algorithm
- Weighted mazes (terrain costs)
- Step-by-step execution mode
- Export solution as image
- Performance comparison charts

---

## 👨‍💻 Author

Enita Hashemi  
BSc (Hons) Computer Science   
Robert Gordon University

---
## License

This project is for educational and portfolio purposes.
