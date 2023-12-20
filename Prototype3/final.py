# Import required libraries
import pika
import random
import tkinter as tk
from tkinter import ttk
import sys
import argparse

#source:Pika,2023
#https://pika.readthedocs.io/en/stable/#
#Pika — pika 1.3.2 documentation. (2023). Readthedocs.io. https://pika.readthedocs.io/en/stable/#

#source : JSON-Python,2023
#https://docs.python.org/3/library/json.html
#json — JSON encoder and decoder. (2023). Python Documentation. https://docs.python.org/3/library/json.html


# Argument parsing for specifying the RabbitMQ server target
parser = argparse.ArgumentParser(
    prog="Tracker"
)
parser.add_argument("target", help="RabbitMQ address")
args = parser.parse_args()

# Import dimensions, Person, and Tracker classes from other modules
from common import dimensions
from person import Player
from tracker import Tracker

#source:tkinter-Python,2023
#https://docs.python.org/3/library/tkinter.html
#tkinter — Python interface to Tcl/Tk. (2023). Python Documentation. https://docs.python.org/3/library/tkinter.html
# GUI application class
class App:
    def __init__(self, root):
        # Initialize the GUI application
        self.root = root
        self.root.title("Player Movement and Contact Tracer")

        # Entry widgets and labels for input fields
        self.board_size_entry = tk.Entry(root)
        self.board_size_entry.grid(row=0, column=1)
        self.board_size_label = tk.Label(root, text="Board Size:")
        self.board_size_label.grid(row=0, column=0)

        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=1, column=1)
        self.id_label = tk.Label(root, text="ID:")
        self.id_label.grid(row=1, column=0)

        self.movespeed_entry = tk.Entry(root)
        self.movespeed_entry.grid(row=2, column=1)
        self.movespeed_label = tk.Label(root, text="Move Speed:")
        self.movespeed_label.grid(row=2, column=0)

        # Buttons to add players and query person interactions
        self.add_player_button = tk.Button(root, text="Add Player", command=self.add_player)
        self.add_player_button.grid(row=3, columnspan=2)

        self.query_button = tk.Button(root, text="Query Person", command=self.query_person)
        self.query_button.grid(row=4, columnspan=2)

        # Canvas to draw the game board
        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.grid(row=5, columnspan=2)

        # Initialize dictionaries to store players and tracker instance
        self.players = {}
        self.tracker = Tracker()

        # Start drawing the game board
        self.draw_board()

    def add_player(self):
        # Add a new player to the game
        target = args.target
        id = self.id_entry.get()
        if id == "":
            id = random.randint(1, 10)

        movespeed = self.movespeed_entry.get()
        if movespeed == "":
            movespeed = random.randint(1, 10) / 10
        movespeed = float(movespeed)
        
        if id not in self.players:
            player = Player(target, id, movespeed)
        else:
            player = self.players[id]
            player.movespeed = movespeed
        self.players[id] = player
        player.start()

    def draw_board(self):
        # Draw the game board and update player positions
        self.canvas.delete("all")
        board_rows, board_columns = dimensions
        tracer = {}
        cell_size = min(400 // board_columns, 400 // board_rows, 50)
        
        # Draw board cells
        for i in range(1, board_rows + 1):
            for j in range(1, board_columns + 1):
                x0, y0 = (i - 1) * cell_size, (j - 1) * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightgray")

        # Draw players on the board and update interactions
        for player in self.players.values():
            x, y = player.x, player.y
            x0, y0 = (x - 1) * cell_size, (y - 1) * cell_size
            x1, y1 = x0 + cell_size, y0 + cell_size
            self.canvas.create_oval(x0, y0, x1, y1, fill="blue")
            
            if (x, y) in tracer.keys():
                self.tracker.add_interaction(player, tracer[(x, y)])
                tracer[(x, y)].append(player)
            else:
                tracer[(x, y)] = [player]
        
        # Schedule to redraw the board after a delay
        self.canvas.after(1000, self.draw_board)

    def query_person(self):
        # Query and display person interactions
        person_id = self.id_entry.get()
        interactions = self.tracker.query_interactions(int(person_id))
        self.display_interactions_window(interactions)

    def display_interactions_window(self, interactions):
        # Display a window with interactions information
        interactions_window = tk.Toplevel(self.root)
        interactions_window.title("Interactions")
        
        for idx, interaction in enumerate(interactions):
            label = tk.Label(interactions_window, text=f"{idx + 1}. {interaction}")
            label.pack(anchor="w")

def main():
    # Initialize the main application
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
