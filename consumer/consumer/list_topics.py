from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
import json
import time

def create_topic(topic_name, num_partitions=1, replication_factor=1):
    """Create a new Kafka topic"""
    admin_client = KafkaAdminClient(
        bootstrap_servers=['localhost:9092'],
        client_id='admin'
    )
    
    try:
        topic = NewTopic(
            name=topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor
        )
        admin_client.create_topics([topic])
        print(f"Created topic: {topic_name}")
    except TopicAlreadyExistsError:
        print(f"Topic {topic_name} already exists")
    finally:
        admin_client.close()

def list_topics():
    """List all Kafka topics"""
    consumer = KafkaConsumer(
        bootstrap_servers=['localhost:9092'],
        group_id='test-group'
    )
    topics = consumer.topics()
    consumer.close()
    return topics

def produce_message(topic, message):
    """Produce a message to a Kafka topic"""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send(topic, message)
    producer.flush()
    producer.close()

def consume_messages(topic):
    """Consume messages from a Kafka topic"""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='test-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print(f"Listening for messages on {topic}...")
    try:
        for message in consumer:
            print(f"Received: {message.value}")
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    # Create a test topic
    topic_name = "test-topic"
    create_topic(topic_name)
    
    # List all topics
    print("\nAvailable topics:")
    for topic in list_topics():
        print(f"- {topic}")
    
    # Produce a test message
    test_message = {"message": "Hello Kafka!", "timestamp": time.time()}
    produce_message(topic_name, test_message)
    print(f"\nProduced message: {test_message}")
    
    # Consume messages
    print("\nStarting consumer...")
    consume_messages(topic_name)