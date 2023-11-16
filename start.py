from get_transactions import get_transactions
from check_anomaly_transfers import check_transfers
from check_anomaly_value import check_anomaly_value
from check_anomaly_hiding import check_anomaly_hiding


api_key = 'f792f335-3a37-443d-8444-e365a775ffe1'
address = input()


transactions = get_transactions(address=address, api_key=api_key, params={'limit': 20})

# Необходимо указать какие транзакции мы проверяем и порог для среднего отклонения
anomaly_value = check_anomaly_value(transactions=transactions, threshold=100)
# В ответ получаем список из всех сумм транзакций их различие между средним арифм., а также сред.ариф., среднее отклонение и разницу между пороговым значением для среднего отклонения и самим средним отклонением

# Необходимо указать какие транзакции мы проверяем, время между транзакциями, которое считается аномальным и адрес, который мы проверяем
anomaly_transfers = check_transfers(transactions=transactions, difference_time=15, address=address)
# В ответ получаем список подозрительных транзакций как from, так и to, то есть и отправленные, и полученные

# Необходимо указать какой кошелек мы проверяем, пороговое значение для суммы трансфера и разницу во времени между трансферами
hiding = check_anomaly_hiding(address=address, value=99, time_difference=5)
# В ответ получаем конечный адрес, который и прислал деньги через левые адреса, а также количество этих адресов

