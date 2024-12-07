import pika
import json

def process_delivery():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='delivery_queue')

    def callback(ch, method, properties, body):
        confirmation = json.loads(body)
        print(f"Delivery Process: Order {confirmation['orderID']} - Payment of ${confirmation['totalAmount']} confirmed.")

    channel.basic_consume(queue='delivery_queue', on_message_callback=callback, auto_ack=True)
    
    print('Waiting for delivery confirmations...')
    channel.start_consuming()

if __name__ == "__main__":
    process_delivery()
