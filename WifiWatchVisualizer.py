from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.channel import Channel
from sys import argv


def callback(ch, method, properties, body: bytearray):
    print(body.decode('utf-8'))


username = argv[1]
password = argv[2]
connection = BlockingConnection(ConnectionParameters(host='::1', credentials=PlainCredentials(username=username, password=password)))
channel: Channel = connection.channel()
channel.queue_declare('spots')
channel.basic_consume(queue='spots', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

