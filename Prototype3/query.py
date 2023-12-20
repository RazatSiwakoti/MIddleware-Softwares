from argparse import ArgumentParser
from structs import Person, Board 
from rabbit import Rabbit  
from json import loads, dumps

#source:Parser-Python,2023
#https://docs.python.org/3/library/argparse.html
#(Argparse — Parser for Command-Line Options, Arguments and Sub-Commands, 2023)

# Argument parsing for specifying the RabbitMQ server target and the user to query for
parser = ArgumentParser(prog="tracker")
parser.add_argument("target", help="Endpoint for middleware")
parser.add_argument("user", help="Username to query for")
args = parser.parse_args()

def main():
    # Initialize the querier Rabbit instance to send the query message
    querier = Rabbit("admin", args.target, "query")
    querier.sender(message=args.user)  # Send the user to query for

    # Initialize the receiver Rabbit instance to consume query responses
    receiver = Rabbit("admin", args.target, "query_response")
    print("start consuming")
    receiver.consumer()  # Start consuming query responses

    #source:freeCodeCamp,2020
#https://www.freecodecamp.org/
if __name__ == "__main__":
    main()
