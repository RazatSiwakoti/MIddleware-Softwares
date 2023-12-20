from rabbit import Rabbit  
from json import dumps 
import argparse

#source:Parser-Python,2023
#https://docs.python.org/3/library/argparse.html
#(Argparse — Parser for Command-Line Options, Arguments and Sub-Commands, 2023)
# Argument parsing for specifying the order details
parser = argparse.ArgumentParser(prog='sendOrder')
parser.add_argument("username", help="Username to connect as")
parser.add_argument("target", help="RabbitMQ server to connect to")
parser.add_argument("action", help="Specify either buy or sell", choices=["buy", "sell"])
parser.add_argument("quantity", help="Amount of shares required", default=100, type=int)
parser.add_argument("price", help="Price of shares", default=100, type=float)

CHANNEL = "orders"  # Communication channel name

def post_order(username, target, action, quantity, price):
    rabbit = Rabbit(username, target, CHANNEL)  # Initialize Rabbit instance for sending orders
    data = {
        "action": action,
        "quantity": quantity,
        "price": price
    }
    rabbit.sender(message=data)  # Send the order data as a message

def main():
    args = parser.parse_args()
    post_order(args.username, args.target, args.action, args.quantity, args.price)

#source:freeCodeCamp,2020
#https://www.freecodecamp.org/
if __name__ == "__main__":
    main()  # Execute the main function if this script is run directly
