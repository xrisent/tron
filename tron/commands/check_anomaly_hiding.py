# from .get_transactions import get_transactions
# import asyncio

# async def check_anomaly_hiding(address, time_difference, api_key):

#     anomaly_addresses = []

#     time_difference = int(time_difference)

#     try:
#         transactions = get_transactions(address=address, api_key=api_key, params={'only_to': True})
#     except:
#         return 'api problem'
    
    
#     async def check_transaction(api_key, transaction, time_difference, new_value, new_address, new_time):
#         anomaly_address = None
#         connections = 1
#         response = None

#         while not anomaly_address:
#             print('b')
#             transactions_1 = get_transactions(new_address, api_key=api_key, params={'min_timestamp': transaction['timestamp']-20, 'max_timestamp': transaction['timestamp']+20})

#             for transaction_1 in transactions_1:
#                 difference = (transaction_1['timestamp'] - new_time)

#                 if int(transaction_1['value']) == new_value and transaction_1['from'] != new_address and difference <= time_difference:
#                     new_address = transaction_1['from']
#                     new_time = transaction_1['timestamp']
#                     new_value = int(transaction_1['value'])
#                     connections += 1
#                 else:
#                     if connections != 1:
#                         response = {
#                             'anomaly_address': transaction_1['from'],
#                             'connections': connections
#                         }
#                     anomaly_address = transaction_1['from']

#         return response


#     tasks = [check_transaction(api_key=api_key, transaction=transaction, time_difference=time_difference,
#                                new_value=int(transaction['value']), new_address=transaction['from'],
#                                new_time=transaction['timestamp']) for transaction in transactions]
    
#     anomaly_addresses = await asyncio.gather(*tasks)

#     if not anomaly_addresses:
#         return {
#             'evaluation': 0
#         }
#     else:
#         return {
#             'anomaly_addresses': anomaly_addresses,
#             'evaluation': (100*len(anomaly_addresses))//len(transactions)
#         }



from .get_transactions import get_transactions

async def check_anomaly_hiding(transactions, address, time_difference, api_key):

    time_difference = int(time_difference)

    anomaly_addresses = []

    for transaction in transactions:
        if transaction['from'] != address:
            anomaly_address = None
            new_address = transaction['from']
            new_time = transaction['timestamp']
            new_value = int(transaction['value'])
            connections = 1

            while not anomaly_address:
                transactions_1 = get_transactions(new_address, api_key=api_key, params={'min_timestamp': transaction['timestamp']-20, 'max_timestamp': transaction['timestamp']+20})

                for transaction_1 in transactions_1:
                    difference = (transaction_1['timestamp'] - new_time)

                    if int(transaction_1['value']) == new_value and transaction_1['from'] != new_address and difference <= time_difference:
                        new_address = transaction_1['from']
                        new_time = transaction_1['timestamp']
                        new_value = int(transaction_1['value'])
                        connections += 1
                    else:
                        if connections != 1:
                            anomaly_addresses.append({
                                'anomaly_address': transaction_1['from'],
                                'connections': connections
                            })
                        anomaly_address = transaction_1['from']
            

    if not anomaly_addresses:
        return {
            'evaluation': 0
        }
    else:
        return {
            'anomaly_addresses': anomaly_addresses,
            'evaluation': (100*len(anomaly_addresses))//len(transactions)
        }