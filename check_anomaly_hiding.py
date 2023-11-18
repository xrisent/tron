from get_transactions import get_transactions
from check_anomaly_transfers import check_transfers
from datetime import datetime

def check_anomaly_hiding(transactions, address, value, time_difference):

    connections = 1
    anomaly_addresses = []
    
    for transaction in transactions:
        if int(transaction['value'])//1000000 == value and transaction['from'] != address:
            anomaly_address = None
            new_address = transaction['from']
            new_time = transaction['time']

            while not anomaly_address:
                transactions_1 = get_transactions(new_address, api_key='f792f335-3a37-443d-8444-e365a775ffe1', params={'limit': 20})

                for transaction_1 in transactions_1:
                    difference = (datetime.strptime(transaction_1['time'], "%Y-%m-%d %H:%M:%S")  - datetime.strptime(new_time, "%Y-%m-%d %H:%M:%S")).total_seconds()

                    if int(transaction_1['value'])//1000000 >= value and transaction_1['from'] != new_address and difference <= time_difference:
                        new_address = transaction_1['from']
                        new_time = transaction_1['time']
                        connections += 1
                    else:
                        anomaly_addresses.append(transaction_1['from'])
                        anomaly_address = transaction_1['from']
                        break

    return anomaly_addresses, connections

