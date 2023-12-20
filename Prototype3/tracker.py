import pika

class Tracker:
    def __init__(self):
        # Initialize the Tracker class
        self.contacts = {}  # Dictionary to store interactions between people
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))  # Connect to RabbitMQ server
        self.channel = self.connection.channel()  # Create a channel
        self.channel.exchange_declare(exchange='logs', exchange_type='topic')  # Declare an exchange
        self.result = self.channel.queue_declare(queue='', exclusive=True)  # Declare a queue with a random name
        self.queue_name = self.result.method.queue  # Get the name of the declared queue
        # Bind the queue to specific routing keys for receiving and responding to queries
        self.channel.queue_bind(exchange='logs', queue=self.queue_name, routing_key='query')
        self.channel.queue_bind(exchange='logs', queue=self.queue_name, routing_key='query-response')
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.handle_query_response, auto_ack=True)

    def handle_query_response(self, ch, method, properties, body):
        # Callback to handle query responses
        person_id = body.decode()
        interactions = self.contacts.get(person_id, [])
        response = ", ".join(interactions)
        # Publish the response to the 'query-response' routing key
        self.channel.basic_publish(
            exchange='logs',
            routing_key='query-response',
            body=response
        )
        print(f"Sent response: {response}")

    def add_interaction(self, person, rest):
        # Add an interaction between people to the contacts dictionary
        pid = int(person.id)
        if pid in self.contacts:
            self.contacts[pid].append([p.id for p in rest])
        else:
            self.contacts[pid] = [[p.id for p in rest]]
        print(pid, self.contacts[pid])

    def query_interactions(self, id):
        # Query and return interactions for a specific person
        return self.contacts.get(id, [])
