import tkinter as tk
from tkinter import ttk
from exchange import Order, start_trader
from sendOrder import post_order
from argparse import ArgumentParser
from threading import Thread
import json
from rabbit import Rabbit

#source:Parser-Python,2023
#https://docs.python.org/3/library/argparse.html
#(Argparse — Parser for Command-Line Options, Arguments and Sub-Commands, 2023)
# Argument parsing for specifying the RabbitMQ server target
parser = ArgumentParser(prog='Stocks')
parser.add_argument("target", help="RabbitMQ server to connect to")


#source : JSON-Python,2023
#https://docs.python.org/3/library/json.html
#json — JSON encoder and decoder. (2023). Python Documentation. https://docs.python.org/3/library/json.html

#source:tkinter-Python,2023
#https://docs.python.org/3/library/tkinter.html
#tkinter — Python interface to Tcl/Tk. (2023). Python Documentation. https://docs.python.org/3/library/tkinter.html

# GUI application class
class App:
    def __init__(self, root, target):
        self.order_book = []
        self.username = "admin"
        self.target = target

        self.trader = Rabbit(self.username, self.target, "orders")

        self.root = root
        self.root.title("Player Movement and Contact Tracer")

        # Label for recent trades
        self.recent_trades_label = tk.Label(root, text="Recent Trades:")
        self.recent_trades_label.pack()

        # Text widget to display recent trades
        self.trades = tk.Text(root, height=5, width=50, state=tk.DISABLED)
        self.trades.pack()

        # Input Section (Single Line)
        self.input_frame = tk.Frame(root)
        self.input_frame.pack()

        # Widgets for price input
        self.price_label = tk.Label(self.input_frame, text="Price:")
        self.price_label.pack(side=tk.LEFT)
        self.price_spinbox = tk.Spinbox(self.input_frame, from_=0, to=100, width=10)
        self.price_spinbox.pack(side=tk.LEFT)

        # Widgets for quantity input
        self.quantity_label = tk.Label(self.input_frame, text="Quantity:")
        self.quantity_label.pack(side=tk.LEFT)
        self.quantity_spinbox = tk.Spinbox(self.input_frame, from_=0, to=100, width=10)
        self.quantity_spinbox.pack(side=tk.LEFT)

        # Buy and Sell buttons
        self.buy_button = tk.Button(self.input_frame, text="BUY", command=self.buy)
        self.sell_button = tk.Button(self.input_frame, text="SELL", command=self.sell)
        self.buy_button.pack(side=tk.LEFT)
        self.sell_button.pack(side=tk.LEFT)

        self.start()

    def __callback(self, ch, method, properties, body):
        # Callback function to process incoming order messages
        current_order = Order(body.decode())
        matching_order = None
        for existing_order in self.order_book:
            if existing_order.action != current_order.action:
                if (existing_order.action == "buy" and existing_order.price >= current_order.price) or \
                   (existing_order.action == "sell" and existing_order.price <= current_order.price):
                    matching_order = existing_order

        if matching_order:
            self.order_book.remove(matching_order)
            trade = json.dumps(dict(
                action=current_order.action,
                quantity=current_order.quantity,
                price=current_order.price
            ))
            self.trades.configure(state=tk.NORMAL)
            self.trades.insert(tk.END, f"{trade}\n")
            self.trades.configure(state=tk.DISABLED)
        else:
            self.order_book.append(current_order)

    def start(self):
        # Start consuming orders using a separate thread
        Thread(target=self.trader.consumer, args=(self.__callback,)).start()

    def get_values(self, action):
        price = self.price_spinbox.get()
        quantity = self.quantity_spinbox.get()
        post_order(self.username, self.target, action, quantity, price)

    def buy(self):
        # Function to handle Buy button click
        self.get_values(action="BUY")

    def sell(self):
        # Function to handle Sell button click
        self.get_values(action="SELL")

def main():
    args = parser.parse_args()
    root = tk.Tk()
    app = App(root, args.target)
    root.mainloop()

#source:freeCodeCamp,2020
#https://www.freecodecamp.org/
if __name__ == "__main__":
    main()
