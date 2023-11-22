import requests
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
        response = requests.get(url=url, headers=headers, params=params)
        transactions_len += len(response.json()['data'])
        fingerprint = response.json()['meta'].get('fingerprint')

        if fingerprint:
            params['fingerprint'] = fingerprint
        else:
            first_transaction = {
                'transaction_id': response.json()['data'][0]['transaction_id'],
                'from': response.json()['data'][0]['from'],
                'to': response.json()['data'][0]['to'],
                'value': response.json()['data'][0]['value'],
                'timestamp': response.json()['data'][0]['block_timestamp'],
                'time': '%s'%datetime.fromtimestamp(response.json()['data'][0]['block_timestamp']/1000),
            }
            last_transaction = {
                'transaction_id': response.json()['data'][transactions_len-1]['transaction_id'],
                'from': response.json()['data'][transactions_len-1]['from'],
                'to': response.json()['data'][transactions_len-1]['to'],
                'value': response.json()['data'][transactions_len-1]['value'],
                'timestamp': response.json()['data'][transactions_len-1]['block_timestamp'],
                'time': '%s'%datetime.fromtimestamp(response.json()['data'][transactions_len-1]['block_timestamp']/1000),
            }
            return {
                'transactions_len': transactions_len, 
                'first_transaction': first_transaction, 
                'last_transaction': last_transaction
                }
