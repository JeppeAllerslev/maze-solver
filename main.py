from solver import Solver

solver = Solver("maze4.bmp")
path = solver.bfs_direct()
solver.save_with_path(path)