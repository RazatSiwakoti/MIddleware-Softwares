#Import Libraries
import tkinter as tk 
import threading  
from rabbit import Rabbit  
from json import loads 
from argparse import ArgumentParser

#source:Parser-Python,2023
#https://docs.python.org/3/library/argparse.html
#(Argparse — Parser for Command-Line Options, Arguments and Sub-Commands, 2023)

# Define command-line arguments
parser = ArgumentParser(prog="Chat")  # Create an argument parser with a program name
parser.add_argument("username", help="Username to connect as")  # Add a required argument: username
parser.add_argument("target", help="RabbitMQ server to connect to")  # Add a required argument: target
args = parser.parse_args()  # Parse the command-line arguments and store them in "args"


#source : JSON-Python,2023
#https://docs.python.org/3/library/json.html
#json — JSON encoder and decoder. (2023). Python Documentation. https://docs.python.org/3/library/json.html

#source:tkinter-Python,2023
#https://docs.python.org/3/library/tkinter.html
#tkinter — Python interface to Tcl/Tk. (2023). Python Documentation. https://docs.python.org/3/library/tkinter.html
# Define the ChatApp class
class ChatApp:

     # Initialize the Rabbit instance, username, and GUI components
    def __init__(self, username, target, channel):
       
        self.rabbit = Rabbit(username, target, channel)
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Chat: {username}")
        
        # Create a text widget to display messages
        self.text_widget = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
        self.text_widget.pack(padx=10, pady=10)
        
        # Create an entry widget for typing messages
        self.entry = tk.Entry(self.root, width=40)
        self.entry.pack(padx=10, pady=(0, 10))
        
        # Create a button to send messages
        self.send_button = tk.Button(self.root, text="Send", command=self.send)
        self.send_button.pack()
        
        # Create a consumer thread to receive messages
        self.consumer_thread = threading.Thread(target=self.rabbit.consumer, args=(self.callback,), name="consumer")
        self.consumer_thread.start()
        
        # Start the GUI main loop
        self.root.mainloop()  


    # Get the message from the entry widget, send it via RabbitMQ, and update the UI
    def send(self):
       
        message = self.entry.get()
        if message:
            self.rabbit.sender(message=message)
            self.entry.delete(0, tk.END)
            self.update_text_widget(f"{self.username}: {message}")

    def callback(self, ch, method, properties, body):
        try:
            data = loads(body.decode())
            msg = f'{data["user"]}: {data["message"]}'
            self.update_text_widget(msg)
        except Exception as e:
            print("Error in callback:", e)

    def update_text_widget(self, text):
        # Update the text widget with a new message and scroll to the end
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, f"\n{text}")
        self.text_widget.see(tk.END)  # Scroll to the end
        self.text_widget.configure(state=tk.DISABLED)

#source:freeCodeCamp,2020
#https://www.freecodecamp.org/
# Entry point of the script
if __name__ == "__main__":
    # Replace with your actual RabbitMQ settings
    username = args.username
    target = args.target
    CHANNEL = "chatroom"

    app = ChatApp(username, target, CHANNEL)  # Create an instance of the ChatApp class
