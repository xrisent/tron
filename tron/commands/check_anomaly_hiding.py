from .get_transactions import get_transactions
from datetime import datetime

def check_anomaly_hiding(transactions, address, time_difference, api_key):

    time_difference = int(time_difference)

    anomaly_addresses = []

    for transaction in transactions:
        if transaction['from'] != address:
            anomaly_address = None
            new_address = transaction['from']
            new_time = transaction['time']
            new_value = int(transaction['value'])
            connections = 1

            while not anomaly_address:
                transactions_1 = get_transactions(new_address, api_key=api_key, params={'min_timestamp': transaction['timestamp']-20, 'max_timestamp': transaction['timestamp']+20})

                for transaction_1 in transactions_1:
                    difference = (datetime.strptime(transaction_1['time'], "%Y-%m-%d %H:%M:%S")  - datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")).total_seconds()

                    if int(transaction_1['value']) == new_value and transaction_1['from'] != new_address and difference <= time_difference:
                        new_address = transaction_1['from']
                        new_time = transaction_1['time']
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

