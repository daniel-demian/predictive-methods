import csv
import threading
import time
import pandas as pd

input_file_path = '../data/data.csv'
output_file_path = '../data/new_data.csv'


with open(input_file_path, 'r', newline='') as input_csvfile:
    reader = csv.reader(input_csvfile)
    header = next(reader)
    with open(output_file_path, 'w', newline='') as output_csvfile:
        writer = csv.writer(output_csvfile)
        writer.writerow(header)

file_lock = threading.Lock()


def process_rows(start_index, step):
    with open("../data/data.csv", "r") as input_file:
        reader = csv.reader(input_file)

        for _ in range(start_index):
            next(reader)

        # Skip the first row
        next(reader, None)

        with open("../data/new_data.csv", "a", newline='', buffering=1) as output_file:
            writer = csv.writer(output_file)

            for row in reader:
                with file_lock:
                    writer.writerow(row)

                print(start_index, row)

                time.sleep(0.3)
                for _ in range(step - 1):
                    next(reader, None)
num_threads = 8

# Create and start threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=process_rows, args=(i, num_threads))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()



