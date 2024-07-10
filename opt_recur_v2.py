import asyncio
import os
import pandas as pd
from web3 import Web3
import datetime
from dotenv import load_dotenv
import aiohttp

load_dotenv()
API_KEY = os.getenv('ETHERSCAN_API_KEY')  # Etherscan API Key
infura_url = os.getenv('INFURA_HTTP_URL')

web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if the connection is successful
if web3.is_connected():
    print("Connected to Ethereum node...")

async def get_transactions(session, address, api_key):
    url = f'https://api.etherscan.io/api?module=account&action=tokentx&address={address}&startblock=0&endblock=999999999&sort=asc&apikey={api_key}'
    async with session.get(url) as response:
        try:
            data = await response.json()
            return data['result']
        except:
            print(f"Error in getting transactions for address {address}")
            return []
        
def convert_timestamp_to_readable(time_stamp):
    dt_object = datetime.datetime.utcfromtimestamp(int(time_stamp))
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

def is_duplicate_event(new_event, existing_events):
    for event in existing_events:
        if all(new_event[key] == event[key] for key in new_event if key != 'layer'):
            return True
    return False

async def process_transactions(session, address, api_key, depth, max_depth, collected_data):
    if depth >= max_depth:
        return collected_data

    transactions = await get_transactions(session, address, api_key)
    tx_count = 0

    for tx in transactions:
        try:
            if tx['to'] == "0x0000000000000000000000000000000000000000":
                continue
            token_decimal = int(tx['tokenDecimal']) if tx['tokenDecimal'] else 0
            amount = int(tx['value']) / (10 ** token_decimal)
            readable_time = convert_timestamp_to_readable(tx['timeStamp'])
            if (amount != 0 and depth == 0 and tx['tokenSymbol'] == 'MCO2' ) or (tx['from'] == address and amount != 0 and depth > 0):
                event_data = {
                    'layer': depth,
                    'BlockNumber': tx['blockNumber'],
                    'TimeStamp': readable_time,
                    'Hash': tx['hash'],
                    'From': tx['from'],
                    'To': tx['to'],
                    'Value': amount,
                    'TokenName':tx['tokenName'],
                    'TokenSymbol':tx['tokenSymbol']
                }
            else:
                continue
            if is_duplicate_event(event_data, collected_data):
                continue
            if tx_count >= 10:
                break
            collected_data.append(event_data)
            print("event_data:", event_data)
            tx_count += 1
            await process_transactions(session, tx['to'], api_key, depth + 1, max_depth, collected_data)
        except Exception as e:
            print(f"Error in transaction {tx['hash']}: {e}")
            continue

    return collected_data

def save_to_csv(data, filename='from_ten_node_mco2.csv'):
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(os.path.join('data', filename), index=False)
    print(f'CSV file {filename} has been saved.')

async def main():
    async with aiohttp.ClientSession() as session:
        collected_data = []
        depth = 0
        max_depth = 3
        INITIAL_ADDRESSES = [
            '0x8fd587b5ea5abd65ad3439d9e58c63222866baa9',
            '0x33e6ab970b5a87a327e6bc13d65760697b4f5527',
            '0x5fff56c053d5428af6c34341535e0f6f9d5ebb4e',
            '0xa9d1e08c7793af67e9d92fe308d5697fb81d3e43',
            '0xb8ba36e591facee901ffd3d5d82df491551ad7ef',
            '0x4a5cf9ecc6fdd4750df92a33ced79d477d9298c8',
            '0x0d0707963952f2fba59dd06f2b425ace40b492fe',
            '0xb8ba36e591facee901ffd3d5d82df491551ad7ef',
            '0xebc18d25d8122da21f73a6bcb78971671f21f6ff',
            '0x5ffF56c053d5428aF6c34341535E0f6f9D5EbB4e'
        ]

        tasks = [process_transactions(session, address, API_KEY, depth, max_depth, collected_data) for address in INITIAL_ADDRESSES]
        await asyncio.gather(*tasks)

        save_to_csv(collected_data)

if __name__ == "__main__":
    asyncio.run(main())