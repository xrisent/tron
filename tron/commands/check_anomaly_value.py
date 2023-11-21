import numpy


async def check_anomaly_value(transactions, minimum_threshold, maximum_threshold):

    values = []
    z_values = []
    count = 0
    
    for transaction in transactions:
        values.append(int(transaction['value'])/1000000)

    average_value = numpy.mean(values)

    average_deviation = numpy.std(values)

    for value in values:
        z_values.append({
            'value': value,
            'z_value': round((value-average_value)/average_deviation, 2)
        })

    for z_value in z_values:
        if z_value['z_value'] >= maximum_threshold or z_value['z_value'] <= minimum_threshold:
            count +=1
    
    if count == 0:
        return {
            'evaluation': 0
        }
    else:
        return {
            'evaluation': (count*100)//len(values),
            'values and z_values': z_values,
            'average_value': average_value,
            'average_deviation': average_deviation
        }