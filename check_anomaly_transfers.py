from datetime import datetime

def check_transfers(transactions, difference_time, address):

    from_list = []
    to_list = []
    anomaly_list_from = []
    anomaly_list_to = []

    for transaction in transactions:
        if transaction['from'] != address:
            from_list.append({
                'transaction_id': transaction['transaction_id'],
                'from_address': transaction['from'],
                'time': transaction['time'],
                'value': transaction['value']
            })
        if transaction['to'] != address:
            to_list.append({
                'transaction_id': transaction['transaction_id'],
                'to_address': transaction['to'],
                'time': transaction['time'],
                'value': transaction['value']
            })
    

    transaction_to_check_from = {
        'transaction_id': None,
        'from_address': None,
        'time': None,
        'value': None
    }

    for transaction in from_list:
        if transaction_to_check_from['from_address'] is not None and transaction_to_check_from['transaction_id'] != transaction['transaction_id']:
            difference = (datetime.strptime(transaction_to_check_from['time'], "%Y-%m-%d %H:%M:%S")  - datetime.strptime(transaction['time'], "%Y-%m-%d %H:%M:%S")).total_seconds()
            if difference <= difference_time:
                anomaly_list_from.append({
                    'transaction_1': transaction_to_check_from,
                    'transaction_2': transaction
                })
            
            transaction_to_check_from['transaction_id'] = transaction['transaction_id']
            transaction_to_check_from['from_address'] = transaction['from_address']
            transaction_to_check_from['time'] = transaction['time']
            transaction_to_check_from['value'] = transaction['value']
        else:
            transaction_to_check_from['transaction_id'] = transaction['transaction_id']
            transaction_to_check_from['from_address'] = transaction['from_address']
            transaction_to_check_from['time'] = transaction['time']
            transaction_to_check_from['value'] = transaction['value']

            

    transaction_to_check_to = {
        'transaction_id': None,
        'to_address': None,
        'time': None,
        'value': None
    }
    
    for transaction in to_list:
        if transaction_to_check_to['to_address'] is not None and transaction_to_check_to['transaction_id'] != transaction['transaction_id']:
            difference = (datetime.strptime(transaction_to_check_to['time'], "%Y-%m-%d %H:%M:%S")  - datetime.strptime(transaction['time'], "%Y-%m-%d %H:%M:%S")).total_seconds()
            if difference <= difference_time:
                anomaly_list_to.append({
                    'transaction_1': transaction_to_check_to,
                    'transaction_2': transaction
                })
            
            transaction_to_check_to['transaction_id'] = transaction['transaction_id']
            transaction_to_check_to['to_address'] = transaction['to_address']
            transaction_to_check_to['time'] = transaction['time']
            transaction_to_check_to['value'] = transaction['value']
        else:
            transaction_to_check_to['transaction_id'] = transaction['transaction_id']
            transaction_to_check_to['to_address'] = transaction['to_address']
            transaction_to_check_to['time'] = transaction['time']            
            transaction_to_check_to['value'] = transaction['value']


    if not anomaly_list_from and not anomaly_list_to:
        return 'Аномалий нету'
    elif not anomaly_list_from:
        return anomaly_list_to
    elif not anomaly_list_to:
        return anomaly_list_from
    else:
        return anomaly_list_from, anomaly_list_to