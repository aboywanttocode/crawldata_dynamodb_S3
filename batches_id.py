import csv
import os

INPUT_FILE = "products-0-200000.csv"
OUTPUT_DIR = "batches"
BATCH_SIZE = 1000

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)

    batch = []
    batch_id = 1

    for row in reader:
        batch.append(row)

        if len(batch) == BATCH_SIZE:
            out_file = f"{OUTPUT_DIR}/batch_{batch_id:03d}.csv"
            with open(out_file, "w", newline="", encoding="utf-8") as out:
                writer = csv.writer(out)
                writer.writerow(header)
                writer.writerows(batch)

            batch = []
            batch_id += 1

    if batch:
        out_file = f"{OUTPUT_DIR}/batch_{batch_id:03d}.csv"
        with open(out_file, "w", newline="", encoding="utf-8") as out:
            writer = csv.writer(out)
            writer.writerow(header)
            writer.writerows(batch)
