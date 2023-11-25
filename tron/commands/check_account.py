import httpx

async def get_account_info(address):
    url = f"https://apilist.tronscanapi.com/api/accountv2?address={address}"
    
    headers = {
        'Content-Type': "application/json"
    }

    response = httpx.get(url, headers=headers)

    for k, v in response.json().items():
        if k == 'redTag':
            return v


