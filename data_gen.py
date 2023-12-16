import csv
import time

out = csv.writer(open("./data/new_data.csv", "w", newline='', buffering=1))
for row in csv.reader(open("./data/data.csv", "r")):
    out.writerow(row)
    print(row)
    time.sleep(1)
