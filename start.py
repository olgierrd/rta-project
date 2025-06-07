import subprocess
import time

def start_kafka_docker():
    try:
        subprocess.run(
            [
                "docker", "run", "-d", "--name", "zookeeper", "-p", "2181:2181",
                "zookeeper:3.4"
            ],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        subprocess.run(
            [
                "docker", "run", "-d", "--name", "kafka", "-p", "9092:9092",
                "-e", "KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181",
                "-e", "KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092",
                "-e", "KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092",
                "-e", "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1",
                "--link", "zookeeper",
                "wurstmeister/kafka"
            ],
            check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
    # Give Kafka a moment to start up
        time.sleep(4)
        print("Kafka and Zookeeper containers started successfully")
        
    except Exception as e:
        print("Could not start Kafka/Zookeeper via Docker:", e)

start_kafka_docker()

# docker stop zookeeper kafka && docker rm zookeeper kafka