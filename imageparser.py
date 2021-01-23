from PIL import Image

class Parser:
    """Parser object for parsing bitmaps into graphs"""

    def __init__(self, image):
        """creates parser object, with associated pillow image"""

        self.image = image
        self.graph = {}
    
    def add_node(self, col, row):
        self.graph[(col,row)] = []

        try:
            if self.image.getpixel((col - 1, row)) == (255,255,255): self.graph[(col,row)].append((col - 1, row))
            if self.image.getpixel((col, row - 1)) == (255,255,255): self.graph[(col,row)].append((col, row - 1))
            if self.image.getpixel((col + 1, row)) == (255,255,255): self.graph[(col,row)].append((col + 1, row))
            if self.image.getpixel((col, row + 1)) == (255,255,255): self.graph[(col,row)].append((col, row + 1))
        except IndexError:
            pass

        #print("Added node: ", (col,row), "With incidence list: ", self.graph[(col,row)])

    def parse_to_graph(self):
        """parses this objects's image into a graph, and returns it"""

        #0,0,0 = black/wall, 255,255,255 = white/passage
        #Coords = (col, row)
        #i = col, j =row
        for i in range(self.image.size[0]):
            for j in range(self.image.size[1]):
                pix = self.image.getpixel((i,j))
                if pix == (255,255,255):
                    self.add_node(i, j)
        return self.graph

    def optimize_graph(self):
        toDelete = []
        for node in list(self.graph.keys()):
            if len(self.graph[node]) == 2:
                adj1 = self.graph[node][0]
                adj2 = self.graph[node][1]
                if adj1[0] == adj2[0] or adj1[1] == adj2[1]:
                    self.graph[adj1].append(adj2)
                    self.graph[adj2].append(adj1)
                    self.graph[adj1].remove(node)
                    self.graph[adj2].remove(node)
                    toDelete.append(node)
        for node in toDelete:
            del self.graph[node]
        return self.graph
