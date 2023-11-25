

def get_finalEvaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient, transfers_coefficient, hiding_coefficient, transactions_len, balance, first_transaction, last_transaction, redTag):

    anomaly_value_evaluation = anomaly_value['evaluation']
    anomaly_transfers_evaluation = anomaly_transfers['evaluation']
    anomaly_hiding_evaluation = anomaly_hiding['evaluation']
    anomaly_relation_evaluation = anomaly_relation['evaluation']

    anomalies_general = (anomaly_value_evaluation*value_coefficient)+(anomaly_transfers_evaluation*transfers_coefficient)+(anomaly_hiding_evaluation*hiding_coefficient)

    coefficient_general = value_coefficient+transfers_coefficient+hiding_coefficient

    if redTag == '':
        redTag = 'Обычный'
    elif redTag == 'Suspicious':
        redTag = 'Подозрительный'
    elif redTag == 'Unsafe':
        redTag = 'Небезопасный'

    finalEvaluation = {
        'finalEvaluation': round(anomalies_general/coefficient_general, 2),
        'transactions': transactions_len,
        'blacklist': anomaly_relation_evaluation,
        'balance': balance,
        'first_transaction': first_transaction,
        'last_transaction': last_transaction,
        'redTag': redTag
    }

    return finalEvaluation

