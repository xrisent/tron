from decouple import config
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse, HttpResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.views.generic import View
import json
from asgiref.sync import async_to_sync


from .commands.check_anomaly_hiding import check_anomaly_hiding
from .commands.check_anomaly_transfers import check_anomaly_transfers
from .commands.check_anomaly_value import check_anomaly_value
from .commands.check_relation import check_relation
from .commands.get_finalEvaluation import get_finalEvaluation
from .commands.get_transactions import get_transactions
from .commands.get_account_balance import get_balance
from .commands.get_transactions_len import get_len
from .commands.get_first_last_transactions import get_first_last_transactions
from .commands.check_account import get_account_info


from core.settings import TRON_SETTINGS

api_key = config('API_TRONGRID_KEY')
api_key_chainalysis = config('CHAINALYSIS_API_KEY')
PARAMS = int(config('PARAMS'))

@swagger_auto_schema(
    methods=['get'],
    manual_parameters=[
        openapi.Parameter(
            'address', openapi.IN_PATH,
            description="Адрес для проверки",
            type=openapi.TYPE_STRING
        ),
    ],
    responses={
        '200': openapi.Response(
            description='Успешная проверка',
            examples={'application/json': {"finalEvaluation": {
                "finalEvaluation": 0.33,
                "transactions": 125,
                "blacklist": 'false',
                "balance": 530,
                "first_transaction": "2020-12-12 19:13:18",
                "last_transaction": "2023-11-05 11:21:06",
                'redTag': 'Обычный'
                },
            "error": 'null',
            "message": 'null'}},
        ),
        '230': openapi.Response(
            description='Транзакции меньше 10',
            examples={'application/json':{'finalEvaluation': None, 'error': None, 'message': 'На этом адресе зарегестрировано меньше 10 транзакций'}},
        ),
        '231': openapi.Response(
            description='Адрес находится в санкционном списке',
            examples={'application/json':{'finalEvaluation': None, 'error': None, 'message': 'Этот адрес находится в санкционном списке'}},
        ),
        '400': openapi.Response(
            description='Неправильный метод запроса',
            examples={'application/json':{'finalEvaluation': None, 'error': 'Bad Request', 'message': None}},
        ),
        '500': openapi.Response(
            description='Внутренняя ошибка сервера',
            examples={'application/json': {'content': {'finalEvaluation': None, 'error': 'Internal server error', 'message': None}}},
        ),
    }
)
@csrf_exempt
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def start_research(request, address):
    try:

        @async_to_sync
        async def inner():
            transactions = await get_transactions(address=address, api_key=api_key, params={ "limit" : PARAMS })
            
            transactions_len = await get_len(address=address, api_key=api_key)
            
            if transactions_len <= 10:
                return JsonResponse({'finalEvaluation': None, 'error': None, 'message': 'На этом адресе зарегестрировано меньше 10 транзакций'}, status=230)
            
            transactions_info = await get_first_last_transactions(address=address, api_key=api_key)
            balance = int(await get_balance(address=address, api_key=api_key))/1000000
            anomaly_relation = await check_relation(address=address, api_key=api_key_chainalysis)

            if anomaly_relation['evaluation'] is True:
                return JsonResponse({'finalEvaluation': None, 'error': None, 'message': 'Этот адрес находится в санкционном списке'}, status=231)

            anomaly_value = await check_anomaly_value(transactions=transactions, minimum_threshold=TRON_SETTINGS['minimum_threshold'], maximum_threshold=TRON_SETTINGS['maximum_threshold'])
            anomaly_transfers = await check_anomaly_transfers(transactions=transactions, difference_time=TRON_SETTINGS['time_difference'], address=address)
            anomaly_hiding = await check_anomaly_hiding(transactions=transactions, address=address, time_difference=TRON_SETTINGS['time_difference'], api_key=api_key)
            redTag = await get_account_info(address=address)

            finalEvaluation = get_finalEvaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient=TRON_SETTINGS['value_coefficient'], transfers_coefficient=TRON_SETTINGS['transfers_coefficient'], hiding_coefficient=TRON_SETTINGS['hiding_coefficient'], transactions_len=transactions_len, balance=balance, first_transaction=transactions_info['first_transaction'], last_transaction=transactions_info['last_transaction'], redTag=redTag)

            response_data = {'finalEvaluation': finalEvaluation, 'error': None, 'message': None}
            json_response = json.dumps(response_data, ensure_ascii=False)

            return HttpResponse(json_response, content_type='application/json; charset=utf-8')

        response = inner()
        return response
            
    except Exception as e:
        return JsonResponse({'finalEvaluation': None, 'error': e, 'message': None}, status=500)