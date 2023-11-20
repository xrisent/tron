# import requests

# def get_len(address, api_key):
#     url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
    
#     headers = {
#         'Content-Type': "application/json",
#         'TRON-PRO-API-KEY': api_key
#     }
#     params = {'limit': 200}
#     count = 1

#     while True:
#         response = requests.get(url=url, headers=headers, params=params)
#         fingerprint = response.json()['meta'].get('fingerprint')

#         if fingerprint:
#             count += 1
#             params['fingerprint'] = fingerprint
#         else:
#             return count*200