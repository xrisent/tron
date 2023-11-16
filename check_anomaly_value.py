import math


def check_anomaly_value(transactions, threshold):

    values = []
    z_values = []
    for_average_deviation = []
    anomaly_list = []
    
    for transaction in transactions:
        values.append(int(transaction['value']))

    average_value = sum(values)/len(values)
    
    for value in values:
        for_average_deviation.append((value-average_value)**2)
        z_values.append({
            'value': value,
            'z_value': value - average_value
        })

    if len(values) > 30:
        average_deviation = math.sqrt(sum(for_average_deviation)/(len(values)-1))
    else:
        average_deviation = math.sqrt(sum(for_average_deviation)/len(values))

    if average_deviation > threshold:
        response = {
            'values and z_values': z_values,
            'average_value': average_value,
            'average_deviation': average_deviation,
            'evaluation': average_deviation - threshold 
        }
        anomaly_list.append(response)
    else:
        response = {
            'values and z_values': z_values,
            'average_value': average_value,
            'average_deviation': average_deviation,
        }

    if not anomaly_list:
        return 'Аномалий нету'
    else:
        return anomaly_list