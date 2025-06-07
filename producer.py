from kafka import KafkaProducer
import json
import random
import numpy as np
import time
from datetime import datetime
from kafka.errors import NoBrokersAvailable

bootstrap_servers = 'localhost:9092'
topic = 'sales'


def generate_sale():
    sale = {
        'sale_id': f'SL{random.randint(1000, 9999)}',
        'profit': round(random.uniform(10, 10000), 2),  
        'transaction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'buyer': random.choice(['Bob', 'Julia', 'Dora', 'Mike']),
        'card_type': np.random.choice(['Visa', 'MasterCard', 'AmEx'], 
                                   p=[0.5, 0.4, 0.1]),
        'item': random.choice(['Laptop', 'Smartphone', 'Tablet', 'Headphones']),
        'quantity': random.randint(1, 5)
        }
    return sale

# Wait for Kafka broker to be available
max_retries = 10
for attempt in range(max_retries):
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8') 
        )
        break
    except NoBrokersAvailable:
        print(f"Kafka broker not available, retrying ({attempt+1}/{max_retries})...")
        time.sleep(3)
else:
    raise RuntimeError("Kafka broker not available after several retries.")

for _ in range(1000):  
    sale = generate_sale()
    producer.send(topic, value=sale) 
    print(f"Sent: {sale}")
    time.sleep(1) 

producer.flush()
producer.close()