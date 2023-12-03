import httpx
from datetime import datetime

async def get_info(address, api_key):
    url = f"https://apilist.tronscanapi.com/api/accountv2?address={address}"
    
    headers = {
        'Content-Type': "application/json"
    }

    response = httpx.get(url, headers=headers)

    data = {}

    for k, v in response.json().items():
        if k == 'totalTransactionCount':
            data['transactions_len'] = v
        else:
            data['transactions_len'] = 0
            
        if k == 'withPriceTokens':
            for dict in v:
                if dict['tokenId'] == 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t':
                    # data['transactions_len'] = dict['transferCount']
                    data['balance'] = int(dict['balance']) / 1000000
                else:
                    data['balance'] = 0
        else:
            data['balance'] = 0
        
        if k == 'redTag':
            data['redTag'] = v

    return data


