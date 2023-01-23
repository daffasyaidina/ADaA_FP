"""
Window used for editing the edges.
"""
import tkinter as tk
from tkinter import messagebox as mb


def main():
    """
    Opens the edit window and returns edits needed.
    """
    root = tk.Tk()
    root.configure(width=500, height=150, bg='white')
    weight = []
    question_label = tk.Label(
        root,
        text="What is the new weight of each of the edges for this node?",
        bg='white')
    down_entry = tk.Entry(root, width=3, bd=3)
    down_label = tk.Label(root, text='Down', bg='white')
    up_entry = tk.Entry(root, width=3, bd=3)
    up_label = tk.Label(root, text='Up', bg='white')
    right_entry = tk.Entry(root, width=3, bd=3)
    right_label = tk.Label(root, text='Right', bg='white')
    left_entry = tk.Entry(root, width=3, bd=3)
    left_label = tk.Label(root, text='Left', bg='white')

    def submit(weight_list):
        """
        Appends the weight entry values to the list and closes the window
        :param weight_list: The list of weights(currently only one weight)
        """

        try:

            weight_list.append(int(down_entry.get()))
            weight_list.append(int(up_entry.get()))
            weight_list.append(int(right_entry.get()))
            weight_list.append(int(left_entry.get()))

        except ValueError:

            mb.showerror(
                'Error',
                'One or more of your inputs are invalid. Please check your inputs and resubmit.')

        root.destroy()

    submitButton = tk.Button(
        root,
        text='Submit',
        bg='lime',
        command=lambda: submit(weight))
    question_label.pack()
    down_entry.pack()
    down_label.pack()
    up_entry.pack()
    up_label.pack()
    right_entry.pack()
    right_label.pack()
    left_entry.pack()
    left_label.pack()
    submitButton.pack()
    question_label.place(x=90, y=20)
    down_label.place(x=145, y=50)
    up_label.place(x=212, y=50)
    right_label.place(x=265, y=50)
    left_label.place(x=330, y=50)
    down_entry.place(x=150, y=70)
    up_entry.place(x=210, y=70)
    right_entry.place(x=270, y=70)
    left_entry.place(x=330, y=70)
    submitButton.place(x=227, y=120)
    root.mainloop()

    if len(weight) != 4:

        weight = None

    return weight
