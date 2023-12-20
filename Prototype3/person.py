import random
import pika
import threading
import time
from common import dimensions  



class Player:
    def __init__(self, target, id, movespeed):
        # Initialize the Player class
        self.target = target  # Target queue name for position updates
        self.id = id  # Player's unique ID
        self.movespeed = movespeed  # Player's movement speed
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Connect to RabbitMQ server
        self.channel = self.connection.channel()  # Create a channel
        self.channel.queue_declare(queue="position")  # Declare the 'position' queue

        self.x, self.y = random.randint(1, dimensions[0]), random.randint(1, dimensions[1])  # Initial position
        self.running = True  # Flag to control the player's running state

    def move_player(self):
        # Function to simulate player movement
        while self.running:
            movement = random.choice([
                (-1, 0), (1, 0), (0, -1), (0, 1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)
            ])

            x_new, y_new = self.x + movement[0], self.y + movement[1]

            # Check if new position is within boundaries
            if 1 <= x_new <= dimensions[0] and 1 <= y_new <= dimensions[1]:
                self.x, self.y = x_new, y_new

            message = f"ID: {self.id}, Position: ({self.x},{self.y})"
            self.channel.basic_publish(exchange='', routing_key=self.target, body=message)

            time.sleep(self.movespeed)

    def start(self):
        # Start a separate thread to simulate player movement
        threading.Thread(target=self.move_player, daemon=True).start()

    def stop(self):
        # Stop the player and close the connection
        self.running = False
        self.connection.close()
