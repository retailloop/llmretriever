import pika
import json

class RabbitMQAdapter:
    def __init__(self, url):
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='simulation_results')

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key='simulation_results', body=json.dumps(message))

    def close(self):
        self.connection.close()