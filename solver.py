from collections import deque
from imageparser import Parser
from PIL import Image
import time

class Solver:
    """Solves given maze-graph"""

    def __init__(self, imageName) -> None:
        '''
        Create solver object

        *imageName, str : name of maze-file in the 'mazes' folder

        '''

        self.graph = {}
        self.imageName = imageName
        self.image = Image.open("mazes/"+imageName).convert(mode='RGB', colors=16)
        self.parser = Parser(self.image)
        self.start, self.stop = self.find_start_stop()

    def current_time_millis(self):
        '''Returns the current time in milliseconds'''

        return time.time() * 1000

    def find_start_stop(self):
        '''Find and return the starting and stopping point of the maze'''
        start, stop = None, None
        for i in range(self.image.size[0]):
           if self.image.getpixel((i, 0)) == (255,255,255): start = (i, 0)
           if self.image.getpixel((i, self.image.size[1] - 1)) == (255,255,255): stop = (i, self.image.size[1] - 1)
        return start, stop

    def create_graph(self, optimize):
        '''
        Create a graph contained in self.graph
        
        *optimize, boolean : wheter or not to optimize the graph nodes
        '''

        startTime = self.current_time_millis()
        self.graph = self.parser.parse_to_graph()
        print("Parsed:", round((self.current_time_millis() - startTime)/1000, 3), "seconds." )

        if optimize:
            startTime = self.current_time_millis() 
            self.graph = self.parser.optimize_graph()
            print("Optimized:", round((self.current_time_millis() - startTime)/1000, 3), "seconds." )

    def save_with_path(self, path):
        '''
        Save the maze with given path drawn in the 'mazes' folder as imageName-solved.bmp

        *path, [(int, int)] : list of nodes in path to draw
        '''

        print("saving...")
        prev = self.stop
        for node in path:
            if node[0] == prev[0]:
                biggest = max(node[1],prev[1])
                for j in range(abs(node[1] - prev[1]) + 1):
                    self.image.putpixel((node[0], biggest - j), (255,0,0))
            else:
                biggest = max(node[0],prev[0])
                for j in range(abs(node[0] - prev[0]) + 1):
                    self.image.putpixel((biggest - j,node[1]), (255,0,0))
            prev = node
        self.image.save("mazes/"+self.imageName.replace(".bmp", "-solved.bmp"))
        print("saved as", self.imageName.replace(".bmp", "-solved.bmp"))

    def bfs_direct(self):
        path = []


    def bfs(self, optimize):
        '''
        Create graph from image and solve it using bfs. Then returns the path as a list of nodes 
        
        *optimize, bool : whether or not to optimize the generated graph
        '''

        if optimize: print("Warning: running bfs with optimized graph does not guarentee shortest solution!")
        self.create_graph(optimize)

        startTime = self.current_time_millis()
        path = []
        visited = [[False for _ in range(self.image.size[0])] for _ in range(self.image.size[1])]
        prev = [[None for _ in range(self.image.size[0])] for _ in range(self.image.size[1])]
        Q = deque([(self.start[0], self.start[1])])
        while len(Q) > 0:
            node = Q.popleft()
            visited[node[0]][node[1]] = True
            if node == (self.stop[0], self.stop[1]): pass
            for adj in self.graph[node]:
                if visited[adj[0]][adj[1]] == False:
                    visited[adj[0]][adj[1]] = True
                    prev[adj[0]][adj[1]] = node
                    Q.append(adj)

        if visited[self.stop[0]][self.stop[1]]:
            node = (self.stop[0], self.stop[1])
            while node != (self.start[0], self.start[1]):
                path.append(node)
                node = prev[node[0]][node[1]]
            path.append((self.start[0], self.start[1]))

        print("Solved:", round((self.current_time_millis() - startTime)/1000, 3), "seconds." )
        print("Path length (nodes):", len(path))
        return path