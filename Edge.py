"""
Edge class
"""


class Edge:
    """
    Class Edge that holds data regarding edges on the grid.
    """

    def __init__(self, source, destination, weight):
        self.source = source
        self.destination = destination
        self.weight = weight

    def get_source(self):
        """
        Returns the source of the edge.
        :return: The source of the edge.
        """
        return self.source

    def get_destination(self):
        """
        Returns the destination of the edge.
        :return: The destination of the edge.
        """
        return self.destination

    def get_weight(self):
        """
        Returns the weight of the edge.
        :return:The weight of the edge.
        """
        return self.weight
