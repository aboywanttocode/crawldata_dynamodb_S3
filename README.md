Tiki Hybrid Crawler 🕷️☁️
Tiki Hybrid Crawler is a high-scale product data scraping tool capable of processing 200,000+ IDs. The project utilizes a Hybrid Architecture to optimize performance and reliability:

Local Worker: Uses curl_cffi to simulate a real browser (TLS Fingerprinting), effectively bypassing Tiki's anti-bot security layers that typically block standard cloud servers (like AWS Lambda).

AWS DynamoDB (Cloud Storage): Amazon's NoSQL database is used for centralized, secure storage, high-speed writing, and auto-scaling capabilities.

# Key Features
Bypass Anti-bot: Implements curl_cffi to mimic Chrome 120, preventing IP blocking.

High Performance: Uses asyncio for multi-threaded processing to maximize network throughput.

Cloud Storage: Direct data push to AWS DynamoDB, ensuring data safety against power outages or local file corruption.

Batch Processing: Automatically iterates through a sequence of CSV files (e.g., batch_001.csv to batch_200.csv).

Robustness: Auto-retry mechanism for network errors and Rate Limit handling (HTTP 429).

 Installation & Configuration
# 1. Prepare AWS DynamoDB
Before running the code, you need to create a table on AWS:

Access the AWS DynamoDB Console.

Select Create table.

Table name: TikiProducts (Must match exactly).

Partition key: id (Type: String).

Capacity settings: Select On-demand (To allow auto-scaling based on traffic).

# 2. Install Libraries
Clone this repository to your local machine and install the required libraries:

Bash

git clone https://github.com/aboywanttocode/crawldata_dynamodb_S3.git
cd project2
pip install -r requirements.txt
(If requirements.txt is missing, create it with the following content):

Plaintext

boto3
pandas
curl_cffi
colorama
asyncio
# 3. Configure AWS Credentials
You need to authorize your machine to write data to DynamoDB.

Method 1 (Recommended): Via AWS CLI Run the following command in your terminal:

Bash

aws configure
# Enter AWS Access Key ID: [Your Key]
# Enter AWS Secret Access Key: [Your Secret Key]
# Enter Default region name: [e.g., us-east-1 or ap-southeast-1]
# Enter Default output format: json
Method 2: Hardcode in script (Not recommended for public GitHub repos) Open main.py and modify the AWS configuration section:

Python

AWS_ACCESS_KEY = "AKIA_YOUR_KEY_HERE"
AWS_SECRET_KEY = "YOUR_SECRET_KEY_HERE"
REGION_NAME = "us-east-1" # Check your specific AWS region
# 4. Prepare Data
Create a folder named batches/ in the project root and place your CSV files containing product IDs there. File naming format:

batch_001.csv

batch_002.csv

...

CSV Structure: The file must have the Product ID in the first column.

# Usage
Run the following command to start the scraping process:

# Bash

python fetch.py

The script will automatically:

Read files sequentially from the batches/ folder.

Scrape data from the Tiki API using the "Local Worker".

Save data directly to DynamoDB.

Report real-time progress (Green text  Saved... indicates success).

# Export Data
Once the process is complete, your data is safely stored on AWS DynamoDB. To download it:

Go to AWS DynamoDB Console -> Tables.

Select TikiProducts -> Exports and streams tab.

Click Export to S3.

Select your destination S3 bucket and desired format (JSON or CSV).

Download the exported file from S3 to your computer.

# Disclaimer
This project is for educational purposes regarding Hybrid Cloud architectures.

Please respect Tiki's terms of service and avoid sending requests too rapidly (The code includes sleep intervals to limit rate).
