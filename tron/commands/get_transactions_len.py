import httpx
from datetime import datetime

async def get_len(address, api_key):
    url = f"https://apilist.tronscanapi.com/api/accountv2?address={address}"
    
    headers = {
        'Content-Type': "application/json"
    }

    response = httpx.get(url, headers=headers)

    for k, v in response.json().items():
        if k == 'withPriceTokens':
            for dict in v:
                if dict['tokenId'] == 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t':
                    return dict['transferCount']


