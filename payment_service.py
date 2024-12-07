import pika
import json

def process_payment():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Creating Q
    channel.queue_declare(queue='payment_queue')
    channel.exchange_declare(exchange='order_fanout', exchange_type='fanout')
    channel.queue_bind(exchange='order_fanout', queue='payment_queue')


    channel.queue_declare(queue='delivery_queue')

    def callback(ch, method, properties, body):  #When new msg arrives
        order = json.loads(body)  #Conversion: JSON => Python
        print(f"Processing payment for Order {order['orderID']} - Amount: ${order['totalAmount']}")

        confirmation_message = json.dumps({
            "orderID": order['orderID'],
            "status": "Payment Confirmed",
            "totalAmount": order['totalAmount']
        })
        channel.basic_publish(exchange='', routing_key='delivery_queue', body=confirmation_message)
        print(f"Sent to delivery queue: {confirmation_message}")

    channel.basic_consume(queue='payment_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for payments...')
    channel.start_consuming()

if __name__ == "__main__":
    process_payment()
