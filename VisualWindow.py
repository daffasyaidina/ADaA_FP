"""
main window asking user for how many rows and columns they want in the grid.
"""

import tkinter as tk
from Constants import DRAW_FUNCS
from tkinter import messagebox as mb


def main():
    """
    Opens a window with a radiobutton giving the user a choice for which algorithm to visualize.
    """
    root = tk.Tk()

    root.configure(width=500, height=112, bg='white')
    visual_label = tk.Label(root, text='Visuals:', bg='white')
    index = tk.IntVar()
    dijkstra_rbutton = tk.Radiobutton(root, text='Dijkstra\'s Algorithm', variable=index, value=0, bg='white')
    bellman_rbutton = tk.Radiobutton(root, text='Bellman-Ford Algorithm', variable=index, value=1, bg='white')

    def submit(visual_index):
        """
        Submits the algorithm that the user wants visualized.
        :param visual_index: The index of the function in DRAW_FUNCS.
        """

        try:

            DRAW_FUNCS[not visual_index] = 0
            DRAW_FUNCS[visual_index] = 1
            root.destroy()

        except ValueError:

            mb.showerror('Error', 'One or more of your inputs are invalid. Please check your inputs and resubmit.')

    submit_button = tk.Button(root, text='Submit', bg='lime', command=lambda: submit(index.get()))
    visual_label.pack()
    visual_label.place(x=183, y=22)
    dijkstra_rbutton.pack()
    dijkstra_rbutton.place(x=243, y=22)
    bellman_rbutton.pack()
    bellman_rbutton.place(x=243, y=42)
    submit_button.pack()
    submit_button.place(x=220, y=82)

    root.mainloop()
