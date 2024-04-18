import random
from datetime import datetime, timedelta
import psycopg2
import time

# Function to generate random data
def generate_random_data(num_records):
    data = []
    current_datetime = datetime.now()
    current_minute = current_datetime.replace(second=0, microsecond=0)
    for i in range(num_records):
        store_id = random.randint(1, 5)
        drink_id = random.randint(1, 8)
        random_seconds = random.randint(0, 59)
        random_time = current_minute + timedelta(seconds=random_seconds)
        datetime_str = random_time.strftime("%Y-%m-%d %H:%M:%S")
        data.append((store_id, drink_id, datetime_str))
        print("Generated Data")
        print("")
    return data

# Function to upload data to the database
def upload_data_to_database(data):
    conn = psycopg2.connect(
        dbname="Starbucks",
        user="postgres",
        password="Zenith1234!",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    for record in data:
        cursor.execute("INSERT INTO Orders (StoreID, DrinkID, Datetime) VALUES (%s, %s, %s)", record)
    conn.commit()
    cursor.close()
    conn.close()
    print("Uploaded Data")

# Main loop
while True:
    # Generate random number of records between 1 and 8
    num_records = random.randint(1, 8)
    
    # Generate random data
    random_data = generate_random_data(num_records)
    
    # Upload data to the database
    upload_data_to_database(random_data)
    
    # Update current minute
    current_minute = datetime.now().replace(second=0, microsecond=0)
    
    # Wait for a minute before generating next batch of records
    time.sleep(60)  # 60 seconds = 1 minute
