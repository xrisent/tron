

def get_finalEvaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient, transfers_coefficient, hiding_coefficient, relation_coefficient, transactions_len, balance):

    anomaly_value_evaluation = anomaly_value['evaluation']
    anomaly_transfers_evaluation = anomaly_transfers['evaluation']
    anomaly_hiding_evaluation = anomaly_hiding['evaluation']
    anomaly_relation_evaluation = anomaly_relation['evaluation']

    anomalies_general = (anomaly_value_evaluation*value_coefficient)+(anomaly_transfers_evaluation*transfers_coefficient)+(anomaly_hiding_evaluation*hiding_coefficient)+(anomaly_relation_evaluation*relation_coefficient)

    coefficient_general = value_coefficient+transfers_coefficient+hiding_coefficient+relation_coefficient

    if anomaly_relation_evaluation == 100:

        finalEvaluation = {
            'finalEvaluation': round(anomalies_general/coefficient_general, 2),
            'transactions': transactions_len,
            'blacklist': True,
            'balance': balance
        }
    else:
        finalEvaluation = {
            'finalEvaluation': round(anomalies_general/coefficient_general, 2),
            'transactions': transactions_len,
            'blacklist': False,
            'balance': balance
        }

    return finalEvaluation

