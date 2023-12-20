from random import randint
from json import dumps

# Dimensions of the board
dimensions = (10, 10)

class Person:
    def __init__(self, id, position) -> None:
        # Initialize the Person class
        self.id = id  # Person's unique identifier
        self.position = position  # Person's position on the board

class Board:
    def __init__(self) -> None:
        # Initialize the Board class
        self.height, self.width = dimensions  # Dimensions of the board
        # Create a nested list to represent positions on the board
        self.positions = [[[] for _ in range(1, self.width + 1)] for _ in range(1, self.height + 1)]

