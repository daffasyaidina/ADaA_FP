"""
External functions used to make, draw, and find positions on grid.
"""
from NegativeCycleException import NegativeCycleException
from Node import Node
from Constants import COLORS
import pygame
from Edge import Edge


def make_grid(rows, width):
    """
    Makes the grid/list of nodes.
    :param rows: The amount of rows.
    :param width: The width of the window.
    :return: The grid/list of nodes.
    """
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def make_grid_keep_edits(rows, oldgrid):
    """
    Makes new grid keeping barriers and start and end.
    :param rows: The amount of rows.
    :param oldgrid: The previous grid.
    :return: The new grid with only barriers, start, and end.
    """
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = oldgrid[i][j]
            if not node.is_state('BARRIER', 'END', 'START', 'EDIT'):
                node.reset()
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    """
    Draws the gridlines on the window.
    :param win: The window being drawn on.
    :param rows: The amount of rows to be drawn.
    :param width: The width of the window.
    """
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, COLORS['LINE'], (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(
                win, COLORS['LINE'], (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    """
    Draws the rectangles/nodes.
    :param win: The window being drawn on.
    :param grid: The list/grid of nodes.
    :param rows: The amount of rows in the grid.
    :param width: The width of the window.
    """
    win.fill(COLORS['NODE'])

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    """
    Converts the position of a click to a row and a column.
    :param pos: The mouse clicked position.
    :param rows: The amount of rows of nodes in the window.
    :param width: The width of the window.
    :rtype: int, int
    :return: The row and column clicked on.
    """
    gap = width // rows
    y_pos, x_pos = pos
    row = y_pos // gap
    col = x_pos // gap
    return row, col


def reconstruct_path(prev, current, draw_func):
    """
    Draws the path found from the algorithm.
    :param prev: The list of nodes in the path.
    :param current: The current node being analyzed;
    the end node since this is only called when end is found.
    :param draw_func: The function used to draw.
    """
    while current in prev:
        current = prev[current]
        if current is not None:
            if not current.is_state('START'):
                current.set_state('PATH')
        draw_func()


def init_single_source(grid, start):
    """
    Initializes the dist and previous dictionaries.
    :param grid: The grid of nodes.
    :param start: The start node.
    :return: The dist and previous dictionaries.
    """
    dist = {node: float('inf') for row in grid for node in row}
    previous = {node: None for row in grid for node in row}
    dist[start] = 0
    return dist, previous


def relax(q, dist, previous, u, v, w):
    """
    The method that relaxes the distances in the dist and previous dictionaries.
    :param q: The queue of nodes.
    :param dist: The dictionary with distances for each node.
    :param previous: The dictionary with previous values for each node.
    :param u: The source node.
    :param v: The destination node.
    :param w: The weight of the edge between the source and the destination.
    :return: A boolean representing whether or not relax was made.
    """
    alt = dist[u] + w
    # Adds distance of current to the distance between neighbors
    if alt < dist[v]:
        dist[v] = alt
        q[v] = alt
        previous[v] = u
        return True
    return False


def dijkstra(draw_func, grid, start, end):
    """
    Dijkstra's algorithm implemented with pygame
    :param draw_func: The function used to draw and update the graph.
    :param grid: The grid/graph of nodes.
    :param start: The start node.
    :param end: The end node.
    :return: A boolean representing whether or not a path is possible between the two nodes.
    """
    commands = 0
    dist, previous = init_single_source(grid, start)
    commands += len(grid) * 2
    node_queue = dist.copy()

    if draw_func:
        pygame.display.set_caption('Checking nearby nodes...')
    else:
        pygame.display.set_caption(
            'Calculating Dijkstra\'s in headless mode...')

    while node_queue:  # Checks if the queue is empty

        for event in pygame.event.get():

            if event.type == pygame.QUIT or pygame.key.get_pressed()[
                    pygame.K_ESCAPE]:
                # If user wants to quit the algorithm midway through the
                # visualization
                pygame.quit()

        current = min(node_queue, key=node_queue.get)
        if dist[current] == float(
                'inf'):  # If the minimum distance is infinity
            break

        del node_queue[current]  # Removes the minimum current from the set

        if current == end:  # If we reached the end
            if draw_func:
                reconstruct_path(previous, current, draw_func)
                # Recolors start and end to avoid loss of start and end
                # positions
                start.set_state('START')
                end.set_state('END')
            return commands, True

        for neighbor in current.neighbors:
            commands += 1
            if relax(node_queue, dist, previous, current, neighbor, current.neighbors[neighbor]) and not (
                neighbor.is_state(
                    'START',
                    'END',
                    'BARRIER')) and draw_func:
                neighbor.set_state('OPEN')

            elif current != start and current != end and current.is_state('OPEN')\
                    and draw_func:  # Closes unneeded nodes
                current.set_state('CLOSED')

        if draw_func:
            draw_func()

    return commands, False


def bellmanford(draw_func, grid, start, end):
    """

    :param draw_func: The function used for drawing. Will be set to none for headless version.
    :param grid: The grid of nodes.
    :param start: The starting node.
    :param end: The ending node.
    :return: A boolean indicating whether or not a shortest path can be found.
    """
    commands = 0
    changes_made = False
    dist = {node: float('inf') for row in grid for node in row}
    commands += len(dist)
    previous = {node: None for row in grid for node in row}
    commands += len(previous)
    dist[start] = 0
    edges = tuple(Edge(node, neighbor, node.neighbors[neighbor]) for row in grid
                  for node in row for neighbor in node.neighbors if not node.is_state('BARRIER'))

    if draw_func:
        pygame.display.set_caption('Mapping each node...')

    else:
        pygame.display.set_caption(
            'Calculating Bellman Ford in Headless Mode...')

    for row in grid:

        for _ in row:

            for event in pygame.event.get():

                if event.type == pygame.QUIT or pygame.key.get_pressed()[
                        pygame.K_ESCAPE]:
                    # If user wants to quit the algorithm midway through the
                    # visualization
                    pygame.quit()

            for edge in edges:

                current = edge.get_source()
                neighbor = edge.get_destination()
                temp_dist = dist[current] + edge.get_weight()
                if temp_dist < dist[neighbor]:
                    dist[neighbor] = temp_dist
                    previous[neighbor] = current
                    if not (
                        neighbor.is_state(
                            'START',
                            'END',
                            'BARRIER')) and draw_func:
                        neighbor.set_state('OPEN')
                        changes_made = True

                if current != start and current != end and current.is_state(
                        'OPEN') and draw_func:
                    # Closes unneeded nodes
                    current.set_state('CLOSED')
                    changes_made = True

            if changes_made and draw_func:
                draw_func()

    commands += len(edges)

    if previous[end] is None:

        return commands, False

    try:

        if draw_func:
            pygame.display.set_caption('Finding Negative Cycles...')

        for edge in edges:

            commands += 1

            for event in pygame.event.get():

                if event.type == pygame.QUIT or pygame.key.get_pressed()[
                        pygame.K_ESCAPE]:
                    # If user wants to quit the algorithm midway through the
                    # visualization
                    pygame.quit()

            current = edge.get_source()
            neighbor = edge.get_destination()
            if dist[current] + edge.weight < dist[neighbor]:
                raise NegativeCycleException

        if draw_func:
            reconstruct_path(previous, end, draw_func)

        return commands, True

    except NegativeCycleException:

        return commands, False
