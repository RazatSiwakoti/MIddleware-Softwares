import pika
import json
import argparse
from rabbit import Rabbit  # Assuming you have a separate module named 'rabbit' that defines the Rabbit class

#source:Parser-Python,2023
#https://docs.python.org/3/library/argparse.html
#(Argparse — Parser for Command-Line Options, Arguments and Sub-Commands, 2023)

# Argument parsing for specifying the target RabbitMQ server
parser = argparse.ArgumentParser(prog='exchange')
parser.add_argument("target", help="RabbitMQ server to connect to")

# List to hold orders in the order book
order_book = []

# Class to represent an order
class Order:
    def __init__(self, order) -> None:
        # Parse the incoming order JSON and initialize order attributes
        data = json.loads(order)
        message = data["message"]
        self.user = data["user"]
        self.action = message["action"].lower()
        self.quantity = message["quantity"]
        self.price = message["price"]

# Callback function to process incoming messages
def callback(ch, method, properties, body):
    global args

    current_order = Order(body.decode())  # Create an Order instance from the received order

    matching_order = None
    for existing_order in order_book:
        # Check if there's a matching order for a trade
        if existing_order.action != current_order.action:
            if (existing_order.action == "buy" and existing_order.price >= current_order.price) or \
               (existing_order.action == "sell" and existing_order.price <= current_order.price):
                matching_order = existing_order

    if matching_order:
        # If a matching order is found, execute a trade
        order_book.remove(matching_order)
        trade = json.dumps(dict(
            action=current_order.action,
            quantity=current_order.quantity,
            price=current_order.price
        ))
        print(trade)  # Print the trade details
        trades.sender(user="admin", message=trade)  # Send trade details to the 'trades' channel
    else:
        # If no matching order, add the current order to the order book
        order_book.append(current_order)

# Function to start the trader with the specified target
def start_trader(target, callback=callback):
    global trades
    trades = Rabbit("admin", target, "trades")  # Initialize Rabbit instance for trades
    orders.consumer(callback=callback)  # Consume orders and execute the provided callback

# Main function
def main():
    global args, orders
    args = parser.parse_args()
    orders = Rabbit("admin", args.target, "orders")  # Initialize Rabbit instance for orders
    start_trader(args.target)  # Start the trader with the specified target

#source:freeCodeCamp,2020
#https://www.freecodecamp.org/
if __name__ == "__main__":
    main()  # Execute the main function if this script is run directly
