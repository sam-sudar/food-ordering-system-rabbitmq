import pika
import json

def receive_notification():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='notification_queue')
    channel.exchange_declare(exchange='order_fanout', exchange_type='fanout')
    channel.queue_bind(exchange='order_fanout', queue='notification_queue')

    def callback(ch, method, properties, body):
        order = json.loads(body)
        print(f"Notification: New order received - {order['orderID']} for {order['customerName']}")


    channel.basic_consume(queue='notification_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for notifications...')
    channel.start_consuming()

if __name__ == "__main__":
    receive_notification()
