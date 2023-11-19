# Система обнаружения аномалий в истории транзакций в сети TRON.

Была разработана система обработки транзакций и аномалий, система должна быть запущена через django, где есть эндпоинт на который отправляется POST запрос

На эндпоинт должны быть отправлены данные адреса кошелька, пороговые значения для Z-оценок в одном из тестов, пороговое значение времени в секундах, а также коэффициенты для финального результата

#### Пример:
    {"address": "TFUBVyRg35WHnjkNFPG7hrzZ8zwcUAR1u1",
    "minimum_threshold": -2,
    "maximum_threshold": 3,
    "time_difference": 13000,
    "value_coefficient": 0.3,
    "transfers_coefficient": 0.4,
    "hiding_coefficient": 0.5,
    "relation_coefficient": 0.6}


## Сбор данных о транзакций:
Сбор данных осуществлялся через API ключ уже отфильтрованных по TRC20 типу
Полученные транзакции форматировались в удобный для дальнейшей работы json-формат, где находятся id транзакции, от кого и кому была сделана транзакция, сумма, а также время в 2 форматах

## Разработка системы обнаружения аномалий:

### Необычно большие или маленькие транзакции
На входе мы должны получить уже отформатированные транзакции, а также пороговые значения для минимальной и максимальной Z-оценки
Данная система работает на numpy, где мы находим среднее арифметическое и среднее отклонение
Далее мы вычисляем Z-оценку для каждой суммы
После этого просчитываем сколько аномальных сумм в истории транзакций и выводим оценку, основанную на процентном соотношении

### Частые и незакономерные движения средств
На входе мы получаем список транзакций, адрес кошелька и пороговую разницу во времени
Для удобной работы список транзакций фильтруется на транзакций, которые были получены и которые были отправлены
Далее мы проверяем эти списки транзакций на факт частых транзакций, где мы указываем пороговую разницу во времени, которая считается аномальной
Оценка также идет на процентном соотношении аномальных транзакций и нормальных транзакций

### Попытки скрыть или затруднить происхождение средств
На входе мы должны получить список транзакций, адрес кошелька и пороговую разницу во времени
Здесь мы проходимся по всем транзакциям и ищем те транзакций, которые были выполнены через "левые" аккаунты, то есть сумма не отличается, а время находится в пороговом значении
Подсчитываем количество таких "левых" аккаунтов, а также находим отправителя
Оценка точно также выдается в процентном соотношении

### Связь с известными мошенниками или преступными организациями
Проверка проходит с помощью API ключа в ChainAlysis
Если адрес находится в санкционном списке, то выставляется оценка 100 баллов

## Оценка опасности
На входе получаем результаты всех тестов на аномалий, а также коэффициенты для каждой аномалии
После выводится финальная оценка на основе этих коэффициентов, а также более подробные результаты тестов на аномалии
