from get_transactions import get_transactions
from check_anomaly_transfers import check_transfers
from check_anomaly_value import check_anomaly_value
from check_anomaly_hiding import check_anomaly_hiding
from check_relation import check_relation
from get_final_evaluation import get_evaluation

api_key = 'f792f335-3a37-443d-8444-e365a775ffe1'
api_key_chainalysis = '546b561c9aba99d9da2ebf042539f28d4ae80b8bcef4bb353ac7e8a2dd79c128'
address = input()


transactions = get_transactions(address=address, api_key=api_key, params={'limit': 20})

# Необходимо указать какие транзакции мы проверяем и порог для среднего отклонения
anomaly_value = check_anomaly_value(transactions=transactions, threshold=1000)
# В ответ получаем список из всех сумм транзакций их различие между средним арифм., а также сред.ариф., среднее отклонение и разницу между пороговым значением для среднего отклонения и самим средним отклонением


# Необходимо указать какие транзакции мы проверяем, время между транзакциями, которое считается аномальным и адрес, который мы проверяем
anomaly_transfers = check_transfers(transactions=transactions, difference_time=15000, address=address)
# В ответ получаем список подозрительных транзакций как from, так и to, то есть и отправленные, и полученные


# Необходимо указать какой кошелек мы проверяем, пороговое значение для суммы трансфера и разницу во времени между трансферами
anomaly_hiding = check_anomaly_hiding(transactions=transactions, address=address, time_difference=1000)
# В ответ получаем конечный адрес, который и прислал деньги через левые адреса, а также количество этих адресов


# Необходимо указать кошелек и api_key для chainalysis
anomaly_relation = check_relation(address=address, api_key=api_key_chainalysis)
# В ответ получаем находится или же нет в санкционных списках

final_evaluation = get_evaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient=0.4, transfers_coefficient=0.3, hiding_coefficient=0.5, relation_coefficient=0.6)

print(final_evaluation)