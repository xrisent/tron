from get_transactions import get_transactions
from check_anomaly_transfers import check_transfers
from datetime import datetime

def check_anomaly_hiding(address, value, time_difference):
    anomaly_address = None
    current_address = address
    connections = 1
    
    while not anomaly_address:
        transactions = get_transactions(current_address, 'f792f335-3a37-443d-8444-e365a775ffe1', params={'limit': 20})
        for transaction in transactions:
            if int(transaction['value']) >= value and transaction['from'] != current_address:
                anomaly_object_transactions = get_transactions(transaction['from'], api_key='f792f335-3a37-443d-8444-e365a775ffe1', params={'limit': 20})
                
                for anomaly_object_transaction in anomaly_object_transactions:
                    difference = (datetime.strptime(anomaly_object_transaction['time'], "%Y-%m-%d %H:%M:%S")  - datetime.strptime(transaction['time'], "%Y-%m-%d %H:%M:%S")).total_seconds()

                    if int(anomaly_object_transaction['value']) == int(transaction['value']) and anomaly_object_transaction['from'] != transaction['from'] and difference <= time_difference:
                        current_address = anomaly_object_transaction['from']
                        connections += 1
                    else:
                        anomaly_address = transaction['from']

    return anomaly_address, connections

        

