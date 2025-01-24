from kafka import KafkaConsumer, KafkaProducer
import json
import time
import sys

def create_producer():
    """Create a Kafka producer"""
    return KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer(topic):
    """Create a Kafka consumer"""
    return KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='test-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def run_producer():
    """Run the producer and get input from user"""
    producer = create_producer()
    print("Producer started. Enter messages (press Ctrl+C to stop):")
    
    try:
        while True:
            message = input("Enter message: ")
            data = {
                "message": message,
                "timestamp": time.time()
            }
            producer.send('test-topic', value=data)
            producer.flush()
            print(f"Sent: {data}")
            
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.close()

def run_consumer():
    """Run the consumer and print received messages"""
    consumer = create_consumer('test-topic')
    print("Consumer started. Waiting for messages... (press Ctrl+C to stop)")
    
    try:
        for message in consumer:
            print(f"Received: {message.value}")
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ['producer', 'consumer']:
        print("Usage: python pubsub.py [producer|consumer]")
        sys.exit(1)

    if sys.argv[1] == 'producer':
        run_producer()
    else:
        run_consumer()