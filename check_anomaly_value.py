import math


def check_anomaly_value(transactions, threshold):

    values = []
    z_values = []
    for_average_deviation = []
    
    for transaction in transactions:
        values.append(int(transaction['value'])/1000000)

    average_value = round(sum(values)/len(values), 2)
    
    for value in values:
        for_average_deviation.append((value-average_value)**2)
        z_values.append({
            'value': value,
            'z_value': value - average_value
        })

    if len(values) > 30:
        average_deviation = round(math.sqrt(sum(for_average_deviation)/(len(values)-1)), 2)
    else:
        average_deviation = round(math.sqrt(sum(for_average_deviation)/len(values)), 2)

    if average_deviation > threshold:
        response = {
            'values and z_values': z_values,
            'average_value': average_value,
            'average_deviation': average_deviation,
            'evaluation': 100 - int((100*threshold)/average_deviation)
        }
        return response
    else:
        return 'Аномалий нету'