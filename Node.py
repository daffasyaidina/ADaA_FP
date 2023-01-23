"""
Node class
"""
from Constants import *
import pygame


class Node:
    """
    Class Node that holds attributes and methods regarding nodes.
    """

    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = COLORS['NODE']
        self.width = width
        self.total_rows = total_rows
        self.left_weight, self.right_weight, self.down_weight, self.up_weight = 1, 1, 1, 1
        self.neighbors = {}

    def get_pos(self):
        """
        Gets the position of the node.
        :return: The row and column of the current node instance.
        """
        return self.row, self.col

    def is_state(self, *states):
        """
        Checks to see if the current node instance is a certain state.
        BARRIER, START, NODE, CLOSED, END, OPEN, PATH, EDIT, LINE
        :return: A boolean representing whether or not the node instance has the given state.
        """

        for state in states:

            if self.color == COLORS[state]:
                return True

        return False

    def reset(self):
        """
        Sets the node's color to the original node color(white).
        """

        self.color = COLORS['NODE']
        self.down_weight = 1
        self.up_weight = 1
        self.right_weight = 1
        self.left_weight = 1

    def set_state(self, state):
        """
        Sets the current node instance to a certain state/color.
        :param state: The state that is to be set to. This state could be any of the below states.
        BARRIER, START, NODE, CLOSED, END, OPEN, PATH, EDIT, LINE
        """

        self.color = COLORS[state]

    def make_edit(self, weight_list):
        """
        Makes edits to nodes weights.
        :param weight_list:
        """
        self.color = COLORS['EDIT']
        self.down_weight = weight_list[0]
        self.up_weight = weight_list[1]
        self.right_weight = weight_list[2]
        self.left_weight = weight_list[3]

    def draw(self, win):
        """
        Draws the node instance on the window.
        :param win: The window being drawn on.
        """
        pygame.draw.rect(
            win,
            self.color,
            (self.x,
             self.y,
             self.width,
             self.width))

    def update_neighbors(self, grid):
        """
        Updates the neighbor list attribute.
        :param grid: The grid/list of nodes.
        """
        self.neighbors = {}

        allowed_nodes = {'Down':
                         self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_state('BARRIER'),
                         'Up':
                         self.row > 0 and not grid[self.row - 1][self.col].is_state('BARRIER'),
                         'Right':
                         self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_state('BARRIER'),
                         'Left':
                         self.col > 0 and not grid[self.row][self.col - 1].is_state('BARRIER')}

        if allowed_nodes['Down']:
            self.neighbors[grid[self.row + 1][self.col]] = self.down_weight

        if allowed_nodes['Up']:
            self.neighbors[grid[self.row - 1][self.col]] = self.up_weight

        if allowed_nodes['Right']:
            self.neighbors[grid[self.row][self.col + 1]] = self.right_weight

        if allowed_nodes['Left']:  # Left
            self.neighbors[grid[self.row][self.col - 1]] = self.left_weight
