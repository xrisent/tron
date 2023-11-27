import httpx
from datetime import datetime
from decouple import config
APPROXIMATE_MAX_TRANSACTIONS_AMOUNT = config('APPROXIMATE_MAX_TRANSACTIONS_AMOUNT')


async def get_transactions(address, api_key, params={}):
    url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
    
    headers = {
        'Content-Type': "application/json",
        'TRON-PRO-API-KEY': api_key
    }

    response = httpx.get(url, headers=headers, params=params)

    data = []

    def format_transactions(response_data):
        for transaction in response_data:
            if transaction['token_info']['symbol'] == 'USDT':
                time = datetime.fromtimestamp(transaction['block_timestamp']/1000)
                data.append({
                    'transaction_id': transaction['transaction_id'],
                    'from': transaction['from'],
                    'to': transaction['to'],
                    'value': transaction['value'],
                    'timestamp': transaction['block_timestamp'],
                    'time': '%s'%time,
                })
    

    while True:
        if len(data) >= int(APPROXIMATE_MAX_TRANSACTIONS_AMOUNT):
             break
        else:
            response = httpx.get(url, headers=headers, params=params)
            response_data = response.json()['data']

            format_transactions(response_data)

            fingerprint = response.json()['meta'].get('fingerprint')
            if fingerprint:
                params['fingerprint'] = fingerprint
            else:
                break

    
    return data