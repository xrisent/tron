

def get_final_evaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient, transfers_coefficient, hiding_coefficient, relation_coefficient):

    anomaly_value_evaluation = anomaly_value['evaluation']
    anomaly_transfers_evaluation = anomaly_transfers['evaluation']
    anomaly_hiding_evaluation = anomaly_hiding['evaluation']
    anomaly_relation_evaluation = anomaly_relation['evaluation']

    anomalies_general = (anomaly_value_evaluation*value_coefficient)+(anomaly_transfers_evaluation*transfers_coefficient)+(anomaly_hiding_evaluation*hiding_coefficient)+(anomaly_relation_evaluation*relation_coefficient)

    coefficient_general = value_coefficient+transfers_coefficient+hiding_coefficient+relation_coefficient

    final_evaluation = {
        'final_evaluation': round(anomalies_general/coefficient_general, 2),
        'anomaly_values': anomaly_value,
        'anomaly_tranfers': anomaly_transfers,
        'anomaly_hidings': anomaly_hiding,
        'anomaly_relation': anomaly_relation, 
        }

    return final_evaluation

