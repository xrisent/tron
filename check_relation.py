import requests

def check_relation(address, api_key):

    headers = {
        'X-API-Key': api_key,
        'Accept': 'application/json',
    }

    response = requests.get(f'https://public.chainalysis.com/api/v1/address/{address}', headers=headers)

    if not response.json()['identifications']:
        return 'Адрес не находится в санкционнах списках'

    return f"{response.json()}\n'Адрес находится в санкционных списках'"