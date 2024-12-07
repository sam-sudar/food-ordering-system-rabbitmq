import pika
import json

def send_order():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='order_fanout', exchange_type='fanout')

    order = {
        "orderID": "5678",
        "customerName": "John Doe",
        "items": ["Pizza", "Pasta"],
        "totalAmount": 30.00
    }

    order_message = json.dumps(order)
    channel.basic_publish(exchange='order_fanout', routing_key='', body=order_message)
    print(f"Order sent: {order_message}")

    connection.close()

if __name__ == "__main__":
    send_order()
