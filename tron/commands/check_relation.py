import requests

def check_relation(address, api_key):

    headers = {
        'X-API-Key': api_key,
        'Accept': 'application/json',
    }

    response = requests.get(f'https://public.chainalysis.com/api/v1/address/{address}', headers=headers)

    if not response.json()['identifications']:
        return {
            'evaluation': 0
        }

    return {
        'sanction': response.json(),
        'evaluation': 100
    }