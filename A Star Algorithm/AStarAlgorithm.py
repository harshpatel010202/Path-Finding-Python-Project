from queue import PriorityQueue
import pygame

WIDTH = 1000
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* SEARCH ALGORITHM")

RED = (255, 0, 0)
LIME = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
NAVY = (0, 0, 128)

class Node:
    def __init__(self, row, col, width, sum_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.sum_rows = sum_rows
        self.width = width
        self.color = BLACK
        self.nearest = []

    def get_its_pos(self):
        return self.row, self.col

    def is_pos_closed(self):
        return self.color == YELLOW

    def is_pos_open(self):
        return self.color == NAVY

    def is_pos_obstacle(self):
        return self.color == WHITE

    def is_pos_commence(self):
        return self.color == YELLOW

    def is_pos_finish(self):
        return self.color == LIME

    def pos_reset(self):
        self.color = BLACK

    def create_pos_path(self):
        self.color = LIME

    def create_pos_obstacle(self):
        self.color = WHITE

    def create_pos_closed(self):
        self.color = YELLOW

    def create_pos_commence(self):
        self.color = RED

    def create_pos_open(self):
        self.color = NAVY

    def create_pos_finish(self):
        self.color = LIME

    def sketch(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_nearest(self, grid):
        self.nearest = []

        if self.row < self.sum_rows - 1 and not grid[self.row + 1][self.col].is_pos_obstacle():
            self.nearest.append(grid[self.row + 1][self.col])

        if self.col < self.sum_rows - 1 and not grid[self.row][self.col + 1].is_pos_obstacle():
            self.nearest.append(grid[self.row][self.col + 1])

        if self.row > 0 and not grid[self.row - 1][self.col].is_pos_obstacle():
            self.nearest.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_pos_obstacle():
            self.nearest.append(grid[self.row][self.col - 1])

    # lt means less than
    def __lt__(self, other):
        return False


def area(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) + abs(y1 - y2)


# algorithm
def algorithm(sketch, grid, commence, finish):
    counter = 0
    available_set = PriorityQueue()
    available_set.put((0, counter, commence))
    evolved = {}
    past_cost_score = {node: float("inf") for row in grid for node in row}
    past_cost_score[commence] = 0
    heru_score = {node: float("inf") for row in grid for node in row}
    heru_score[commence] = area(commence.get_its_pos(), finish.get_its_pos())

    available_set_hash = {commence}

    while not available_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        currentNode = available_set.get()[2]
        available_set_hash.remove(currentNode)

        if currentNode == finish:
            final_step(evolved, finish, sketch)
            finish.create_pos_finish()
            return True

        for nearest in currentNode.nearest:
            node_past_cost_score = past_cost_score[currentNode] + 1

            if node_past_cost_score < past_cost_score[nearest]:
                evolved[nearest] = currentNode
                past_cost_score[nearest] = node_past_cost_score
                heru_score[nearest] = node_past_cost_score + area(nearest.get_its_pos(), finish.get_its_pos())

                if nearest not in available_set_hash:
                    counter += 1
                    available_set.put((heru_score[nearest], counter, nearest))
                    available_set_hash.add(nearest)
                    nearest.create_pos_open()

        sketch()

        if currentNode != commence:
            currentNode.create_pos_closed()

    return False


def create_its_grid(MAKE_ROWS, width):
    grid = []
    space = width // MAKE_ROWS
    for i in range(MAKE_ROWS):
        grid.append([])
        for j in range(MAKE_ROWS):
            node = Node(i, j, space, MAKE_ROWS)
            grid[i].append(node)

    return grid


def sketch_grid(win, MAKE_ROWS, width):
    space = width // MAKE_ROWS
    for i in range(MAKE_ROWS):
        pygame.draw.line(win, GRAY, (0, i * space), (width, i * space))
        for j in range(MAKE_ROWS):
            pygame.draw.line(win, GRAY, (j * space, 0), (j * space, width))


def sketch(win, grid, MAKE_ROWS, width):
    win.fill(BLACK)

    for row in grid:
        for node in row:
            node.sketch(win)

    sketch_grid(win, MAKE_ROWS, width)
    pygame.display.update()


def pos_clicked(pos, MAKE_ROWS, width):
    space = width // MAKE_ROWS
    y, x = pos

    row = y // space
    col = x // space

    return row, col

# final step
def final_step(evolved, currentNode, sketch):
    while currentNode in evolved:
        currentNode = evolved[currentNode]
        currentNode.create_pos_path()
        sketch()


def main(win, width):
    MAKE_ROWS = 40
    grid = create_its_grid(MAKE_ROWS, width)

    #SET BOTH COMMENCE AND FINISH TO NONE#
    commence = None
    finish = None

    run = True

    #THIS MEANS WHILE IT IS RUNNING THE FOLLOWING THING IN THE LOOP WILL OCCUR
    while run:

        sketch(win, grid, MAKE_ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #TO POSITION COMMENCE, FINISH AND OBSTACLES POSITIONS --> CAN BE DONE USING LEFT CLICK
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = pos_clicked(pos, MAKE_ROWS, width)
                node = grid[row][col]
                if not commence and node != finish:
                    commence = node
                    commence.create_pos_commence()

                elif not finish and node != commence:
                    finish = node
                    finish.create_pos_finish()

                elif node != finish and node != commence:
                    node.create_pos_obstacle()

            #TO ERASE THE COMMENCE, FINISH AND OBSTACLES POSITIONS --> CAN BE DONE USING RIGHT CLICK
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = pos_clicked(pos, MAKE_ROWS, width)
                node = grid[row][col]
                node.pos_reset()

                if node == commence:
                    commence = None
                elif node == finish:
                    finish = None

            # if space bar is clicked
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and commence and finish:
                    for row in grid:
                        for node in row:
                            node.update_nearest(grid)

                    algorithm(lambda: sketch(win, grid, MAKE_ROWS, width), grid, commence, finish)

                # if space bar is clicked
                if event.key == pygame.K_c:
                    commence = None
                    finish = None
                    grid = create_its_grid(MAKE_ROWS, width)

    pygame.quit()


main(WINDOW, WIDTH)
