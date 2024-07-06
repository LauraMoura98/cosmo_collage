import requests 
import os
from dotenv import load_dotenv

load_dotenv()
polygon_api_key = os.getenv('POLYGON_API')
wallet_address = '0x15572b0f6e6DD6ACFC083de45A390827F431d20d'

def get_transfers(address: str, key: str):
    url = f'https://api.polygonscan.com/api?module=account&action=tokennfttx&' \
          f'address={address}&startblock=0&endblock=99999999&page=1&offset=1000&' \
          f'sort=desc&apikey={key}'

    transfer_result = requests.get(url).json()
    return transfer_result['result']


def get_token_id():
    get_polygon_transfers = get_transfers(wallet_address, polygon_api_key)
    transfers = []
    seen_token_ids = set()
    count = 0
    for transfer in get_polygon_transfers:
        if transfer['to'].lower() == wallet_address.lower() and transfer['tokenID'] not in seen_token_ids:
            transfers.append(transfer['tokenID'])
            seen_token_ids.add(transfer['tokenID'])
            count += 1
            if count == 10:
                break
    return transfers

print(get_token_id())