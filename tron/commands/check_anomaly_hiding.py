from .get_transactions import get_transactions

async def check_anomaly_hiding(transactions, address, time_difference, api_key):

    time_difference = int(time_difference)

    anomaly_addresses = set()
    transactions_cache = {}

    for transaction in transactions:
        if transaction['from'] != address:
            anomaly_address = None
            new_address = transaction['from']
            new_time = transaction['timestamp']
            new_value = int(transaction['value'])
            connections = 1

            while not anomaly_address:
                if new_address not in transactions_cache:
                    transactions_1 = await get_transactions(new_address, api_key=api_key, params={'min_timestamp': transaction['timestamp'] - 20, 'max_timestamp': transaction['timestamp'] + 20})
                    transactions_cache[new_address] = transactions_1
                else:
                    transactions_1 = transactions_cache[new_address]

                for transaction_1 in transactions_1:
                    difference = (transaction_1['timestamp'] - new_time)

                    if int(transaction_1['value']) == new_value and transaction_1['from'] != new_address and difference <= time_difference:
                        new_address = transaction_1['from']
                        new_time = transaction_1['timestamp']
                        new_value = int(transaction_1['value'])
                        connections += 1
                    else:
                        if connections != 1:
                            anomaly_addresses.add({
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