import httpx
from datetime import datetime

async def get_first_last_transactions(address, api_key):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
    
    headers = {
        'Content-Type': "application/json",
        'TRON-PRO-API-KEY': api_key
    }
    params_first = {'limit': 1, 'order_by': 'block_timestamp,asc'}
    params_last = {'limit': 1, 'order_by': 'block_timestamp,desc'}

    response_first = httpx.get(url=url, headers=headers, params=params_first)
    response_last = httpx.get(url=url, headers=headers, params=params_last)

    first_transaction = '%s'%datetime.fromtimestamp(response_first.json()['data'][0]['block_timestamp']/1000)
    last_transaction = '%s'%datetime.fromtimestamp(response_last.json()['data'][0]['block_timestamp']/1000)

    return {
        'first_transaction': first_transaction,
        'last_transaction': last_transaction
    }