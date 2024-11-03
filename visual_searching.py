import pygame
import sys
from queue import PriorityQueue
import queue

WIDTH = 800
HEIGHT = 800
SCREEN = pygame.display.set_mode(size=(WIDTH,HEIGHT))
pygame.display.set_caption("Visual searching     Press:    1:A* Algorithm    2:DFS      3:BFS     4:Dijkstra")
pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, column, width, total_rows) :
        self.row = row
        self.column = column
        self.width = width
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows


    def get_position(self):
        return self.x, self.y
    

    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == TURQUOISE
    
    def is_obstacle(self):
        return self.color == BLACK
    
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_notVisited(self):
        return self.color == WHITE
    
    # setters
    def set_start(self):
        self.color = ORANGE
    
    def set_end(self):
        self.color = TURQUOISE

    def set_obstacle(self):
        self.color = BLACK
    
    def set_closed(self):
        self.color = RED

    def set_open(self):
        self.color = GREEN

    def reset(self):
        self.color = WHITE

    def set_final_path(self):
        self.color = PURPLE

    def update_neighbors(self,grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_obstacle(): # down
            self.neighbors.append(grid[self.row + 1][self.column])
        if self.row > 0 and not grid[self.row - 1][self.column].is_obstacle(): # top
            self.neighbors.append(grid[self.row - 1][self.column])
        if self.column > 0 and not grid[self.row][self.column - 1].is_obstacle(): # left
            self.neighbors.append(grid[self.row][self.column - 1])
        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_obstacle(): # right
            self.neighbors.append(grid[self.row][self.column + 1])    

    def get_neighbors(self):
        return self.neighbors
    

    def draw (self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.width))
    

def create_grid(rows, width):
    grid = []
    width_cell = width // rows
    for i in range (rows):
        grid.append([])
        for j in range (rows):
            node = Node(i, j, width_cell, rows)
            grid[i].append(node)

    return grid


def draw_grid(screen, rows, width):
    width_cell = width // rows
    for i in range (rows):
        pygame.draw.line(screen,GREY,(0, i * width_cell), (width, i * width_cell))
        for j in range (rows):
            pygame.draw.line(screen, GREY,(j * width_cell,0), (j * width_cell, width))


def draw(screen, grid, rows, width):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(screen)

    draw_grid(screen, rows, width)
    pygame.display.update()


def get_mouse_position(pos, rows, width):
    x,y = pos
    width_cell = width // rows

    row = x // width_cell
    col = y // width_cell
    return row, col


def heuristic(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs (x2-x1) + abs(y2-y1)


def recontructPath(parent, end, draw):
    current_node = end
    current_node.set_final_path()
    path = []
    while current_node in parent:
        current_node = parent[current_node]
        if current_node.is_start():
            current_node.set_final_path()
            path.append(current_node)
            break
        current_node.set_final_path()
        path.append(current_node)
        draw()

    print("Start")
    path.reverse()
    for current_node in path:
        print(f"({current_node.column}, {current_node.row})")
    print("Goal")



def DFS (draw, start, end):
    stack = []
    visited = []

    stack.append(start)
    visited.append(start)

    parent ={}
    parent[start] = None

    while stack:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        current_node = stack.pop()

        if current_node == end:
            recontructPath(parent, end , draw)
            return
        

        for neighbor in current_node.get_neighbors():
            if neighbor not in visited:
                neighbor.set_open()
                visited.append(neighbor)
                stack.append(neighbor)
                parent[neighbor] = current_node

        draw()
        if current_node != start:
            current_node.set_closed()


def BFS(draw, start, end):
    q = queue.Queue()
    visited = []

    q.put(start)
    visited.append(start)

    parent ={}
    parent[start] = None

    while not q.empty():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        current_node = q.get()

        if current_node == end:
            recontructPath(parent, end , draw)
            return
        

        for neighbor in current_node.get_neighbors():
            if neighbor not in visited:
                neighbor.set_open()
                visited.append(neighbor)
                q.put(neighbor)
                parent[neighbor] = current_node

        draw()

        if current_node != start:
            current_node.set_closed()




def aStarAlgorithm(draw, start, end, grid):
    # print(f"({start.row}, {start.column})")
    count = 0
    frontier = PriorityQueue()
    frontier.put((0,count, start))
    parent ={}
    parent[start] = None
    g_score = {node: float("inf")  for row in grid for node in row}
    g_score[start] = 0
    h_score = {node: float("inf")  for row in grid for node in row}
    h_score[start] = 0
    f_score = {node: float("inf")  for row in grid for node in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())


    visited = {start}


    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

        current_node= frontier.get()[2]
        visited.remove(current_node)

        if current_node == end:
            recontructPath(parent, end, draw)
            return
        
        
        for neighbor in current_node.get_neighbors():

            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbor]:
                parent[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in visited:
                    count = count + 1
                    frontier.put((f_score[neighbor], count, neighbor))
                    visited.add(neighbor)
                    neighbor.set_open()

        draw()

        if current_node != start:
            current_node.set_closed()


def Dijkstra(draw, start , end , grid):
    count = 0
    frontier = PriorityQueue()
    frontier.put((0,count, start))
    parent ={}
    parent[start] = None
    g_score = {node: float("inf")  for row in grid for node in row}
    g_score[start] = 0



    visited = {start}


    while not frontier.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()

        current_node= frontier.get()[2]
        visited.remove(current_node)

        if current_node == end:
            recontructPath(parent, end, draw)
            return
        
        
        for neighbor in current_node.get_neighbors():

            temp_g_score = g_score[current_node] + 1

            if temp_g_score < g_score[neighbor]:
                parent[neighbor] = current_node
                g_score[neighbor] = temp_g_score
                if neighbor not in visited:
                    count = count + 1
                    frontier.put((g_score[neighbor], count, neighbor))
                    visited.add(neighbor)
                    neighbor.set_open()

        draw()

        if current_node != start:
            current_node.set_closed()
   




def main(screen, width):
    ROWS = 50
    grid = create_grid(ROWS, width)

    start = None
    end = None

    run = True
    algorithm_started = False

    algorithm_chosen = None

    while run:
        draw(screen, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if algorithm_started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    # print(f"({node.row}, {node.column})")
                    start.set_start()
                
                elif not end and node != start:
                    end = node
                    end.set_end()

                
                elif node != start and node != end:
                    node.set_obstacle()
            
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_mouse_position(pos, ROWS, width)
                node = grid[row][col]

                if node.is_start():
                    start = None
                elif node.is_end():
                    end = None

                node.reset()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    algorithm_chosen = lambda: aStarAlgorithm(lambda: draw(screen, grid, ROWS, width), start, end, grid)
                    pygame.display.set_caption("Visual Searching - A* Algorithm")
                elif event.key == pygame.K_2:
                    algorithm_chosen = lambda: DFS(lambda: draw(screen, grid, ROWS, width), start, end)
                    pygame.display.set_caption("Visual Searching - DFS")
                elif event.key == pygame.K_3:
                    algorithm_chosen = lambda: BFS(lambda: draw(screen, grid, ROWS, width), start, end)
                    pygame.display.set_caption("Visual Searching - BFS")
                elif event.key == pygame.K_4:
                    algorithm_chosen = lambda: Dijkstra(lambda: draw(screen, grid, ROWS, width), start, end, grid)
                    pygame.display.set_caption("Visual Searching - Dijkstra")
                
                if event.key == pygame.K_SPACE and start and end and algorithm_chosen:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm_chosen()  
                    algorithm_started = True
                
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(SCREEN,WIDTH)