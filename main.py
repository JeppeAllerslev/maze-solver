from solver import Solver

solver = Solver("maze3.bmp")
path = solver.bfs(True)
solver.save_with_path(path)