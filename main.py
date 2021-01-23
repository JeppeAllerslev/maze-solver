from solver import Solver

solver = Solver("maze3.bmp")
path = solver.bfs(False)
solver.save_with_path(path)