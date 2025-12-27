import asyncio
import boto3
import pandas as pd
import time
import os
from decimal import Decimal
from curl_cffi.requests import AsyncSession, BrowserType
from botocore.exceptions import ClientError
from colorama import init, Fore

init(autoreset=True)


BATCH_FOLDER = "batches"      # Folder containing CSV batch files
START_BATCH = 1               # Start from batch_001.csv
END_BATCH = 200               # End at batch_200.csv
TABLE_NAME = "TikiProducts"
CONCURRENT_LIMIT = 5          # Concurrent requests per batch file


AWS_ACCESS_KEY = None
AWS_SECRET_KEY = None
REGION_NAME = "us-east-1"

try:
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
    else:
        dynamodb = boto3.resource("dynamodb", region_name=REGION_NAME)

    table = dynamodb.Table(TABLE_NAME)
    print(Fore.GREEN + " Connected to DynamoDB successfully!")
except Exception as e:
    print(Fore.RED + f" AWS connection error: {str(e)}")
    exit()


async def fetch_and_push(session, pid, semaphore):
    url = f"https://tiki.vn/api/v2/products/{pid}"

    async with semaphore:
        for attempt in range(3):
            try:
                await asyncio.sleep(0.5)

                response = await session.get(
                    url,
                    impersonate=BrowserType.chrome120,
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()
                    rating_val = data.get("rating_average", 0)

                    item = {
                        "id": str(data.get("id")),
                        "name": data.get("name"),
                        "price": int(data.get("price", 0)) if data.get("price") else 0,
                        "rating": Decimal(str(rating_val)),
                        "updated_at": int(time.time()),
                        "batch_source": "hybrid_crawler"
                    }

                    try:
                        table.put_item(Item=item)
                        print(Fore.GREEN + f" Saved product {pid}")
                        return True
                    except Exception as db_err:
                        print(Fore.RED + f" DynamoDB error for ID {pid}: {db_err}")
                        return False

                elif response.status_code == 404:
                    print(Fore.YELLOW + f" Product not found (404): {pid}")
                    return False

                elif response.status_code == 429:
                    print(Fore.MAGENTA + f" Rate limited for {pid}. Sleeping 5s...")
                    await asyncio.sleep(5)

                else:
                    await asyncio.sleep(1)

            except Exception as e:
                print(Fore.RED + f" Request error for ID {pid}: {e}")
                await asyncio.sleep(1)

        return False


async def process_batch_file(file_path, batch_num):
    print(Fore.CYAN + f"\n Opening batch file: {file_path}")

    if not os.path.exists(file_path):
        print(Fore.RED + f" File not found: {file_path}. Skipping...")
        return

    try:
        df = pd.read_csv(file_path)
        all_ids = df.iloc[:, 0].astype(str).tolist()
    except Exception as e:
        print(Fore.RED + f" Failed to read CSV {file_path}: {e}")
        return

    print(Fore.CYAN + f" Batch {batch_num}: Processing {len(all_ids)} product IDs")

    semaphore = asyncio.Semaphore(CONCURRENT_LIMIT)

    async with AsyncSession() as session:
        tasks = [fetch_and_push(session, pid, semaphore) for pid in all_ids]
        await asyncio.gather(*tasks)

    print(Fore.GREEN + f" Finished batch {batch_num}")

async def main():
    total_start = time.time()

    for i in range(START_BATCH, END_BATCH + 1):
        file_name = f"batch_{i:03d}.csv"
        file_path = os.path.join(BATCH_FOLDER, file_name)

        await process_batch_file(file_path, i)

        print(Fore.BLUE + " Sleeping 2 seconds before next batch...")
        time.sleep(2)

    total_end = time.time()
    duration = total_end - total_start

    print(
        Fore.GREEN
        + f"\n ALL BATCHES COMPLETED ({START_BATCH}-{END_BATCH}) "
        + f"in {duration / 60:.2f} minutes "
    )

if __name__ == "__main__":
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
