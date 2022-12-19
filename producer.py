import csv
from time import sleep
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# Define function to load avro schema
def load_avro_schema_from_file():
    key_schema = avro.load("bitcoin_price_key.avsc")
    value_schema = avro.load("bitcoin_price_value.avsc")
    return key_schema, value_schema

# Define function to send each record of dataset to kafka broker
def send_record():
    key_schema, value_schema = load_avro_schema_from_file()

    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081",
        "acks": "1"
    } # to broker

    # define schema to avro producer
    producer = AvroProducer(producer_config,
                            default_key_schema=key_schema,
                            default_value_schema=value_schema)

    # open the dataset
    file = open('data/bitcoin_price.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)

    for row in csvreader:
        key = {"Date": (row[0])}
        value = {"Date": (row[0]),
                 "Open": float(row[1]),
                 "High": float(row[2]),
                 "Low": float(row[3]),
                 "Close": float(row[4]),
                 "Volume": (row[5]),
                 "MarketCap": (row[6])}

        try:
            # publish kafka topic
            producer.produce(topic='kafka_avroproducer', key=key, value=value)
        except Exception as e:
            print(f"Exception while producing record value - {value}: {e}")
        else:
            print(f"Successfully producing record value - {value}")

        producer.flush()
        sleep(2)

if __name__ == "__main__":
    send_record()