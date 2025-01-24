from kafka import KafkaProducer
import json
import time
import random

class SongEventProducer:
    def __init__(self, bootstrap_servers=['localhost:9092']):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
    def generate_song_event(self):
        return {
            'song_id': random.randint(1, 1000),
            'timestamp': int(time.time()),
            'user_id': random.randint(1, 10000),
            'duration': random.randint(30, 300)
        }
        
    def send_events(self, topic='song-events', interval=1):
        while True:
            event = self.generate_song_event()
            self.producer.send(topic, value=event)
            time.sleep(interval)

if __name__ == "__main__":
    producer = SongEventProducer()
    producer.send_events()