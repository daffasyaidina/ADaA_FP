"""
Holds constants such as colors.
"""
ROWS = 50
WIDTH = 800
DRAW_FUNCS = [1, 0]  # 0th index is initially 1, due to dijkstra's being the preferred visualized algorithm.
COLORS = {'BARRIER': (44, 44, 46),
          'START': (48, 219, 91),
          'NODE':(72, 72, 74),
          'CLOSED':(48, 209 , 88),
          'END': (255, 214, 10),
          'OPEN': (255, 69, 58),
          'PATH': (10, 132, 255),
          'EDIT': (0, 0, 255),
          'LINE': (28, 28, 30)}
