import httpx
from datetime import datetime

async def get_len(address, api_key):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
    
    headers = {
        'Content-Type': "application/json",
        'TRON-PRO-API-KEY': api_key
    }
    params = {'limit': 200}
    transactions_len = 0

    while True:
        response = httpx.get(url=url, headers=headers, params=params)
        for transaction in response.json()['data']:
            if transaction['token_info']['symbol'] == 'USDT':
                transactions_len += 1
        fingerprint = response.json()['meta'].get('fingerprint')

        if fingerprint:
            params['fingerprint'] = fingerprint
        else:
            return transactions_len 
