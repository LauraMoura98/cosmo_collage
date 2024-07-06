import requests 
import os
from dotenv import load_dotenv
import json
load_dotenv()

polygon_api_key = os.getenv('POLYGON_API')
opensea_api_key = os.getenv('OPEN_SEA_API')
contract_address = os.getenv('COSMO_CONTRACT_ADDRESS')
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
    return transfers


def get_objekt_info(contract: str, key: str, token_id: str):
    url = f'https://api.opensea.io/api/v2/chain/matic/contract/{contract}/nfts/{token_id}'
    headers = {
        "accept": "application/json",
        "x-api-key": key
    }
    response = requests.get(url, headers=headers)
    return response.json()

def create_objekts_dict():
    token_ids = get_token_id()
    objekts = {}
    for i in range(10):
        objekt_info = get_objekt_info(contract_address, opensea_api_key, token_ids[i])
        nft_data = objekt_info['nft']
        objekts[nft_data['identifier']] = {
            'name': nft_data['name'],
            'image_url': nft_data['image_url']
        }
    return objekts

objekts = create_objekts_dict()

with open('objekts.json', 'w') as json_file:
    json.dump(objekts, json_file, indent=4)

print("Arquivo JSON criado com sucesso.")