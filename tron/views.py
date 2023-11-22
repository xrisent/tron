from decouple import config
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.views.generic import View

from .commands.check_anomaly_hiding import check_anomaly_hiding
from .commands.check_anomaly_transfers import check_anomaly_transfers
from .commands.check_anomaly_value import check_anomaly_value
from .commands.check_relation import check_relation
from .commands.get_finalEvaluation import get_finalEvaluation
from .commands.get_transactions import get_transactions
from .commands.get_account_balance import get_balance
from .commands.get_transactions_len import get_len

from asgiref.sync import async_to_sync

from core.settings import TRON_SETTINGS

api_key = config('API_TRONGRID_KEY')
api_key_chainalysis = config('CHAINALYSIS_API_KEY')

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
            description='Successful response',
            content={'application/json': {'example': {'evaluation': 0.85}}},
        ),
        '400': openapi.Response(
            description='Bad request',
            content={'application/json': {'example': {'error': 'Invalid data'}}},
        ),
    }
)
@csrf_exempt
@api_view(['GET'])
@renderer_classes([JSONRenderer])
def start_research(request, address):

    @async_to_sync
    async def inner():
        try:
            transactions = await get_transactions(address=address, api_key=api_key, params=TRON_SETTINGS['params'])
        except:
            return JsonResponse({'error': 'Invalid address'})
        
        transactions_info = await get_len(address=address, api_key=api_key)
        
        if transactions_info['transactions_len'] <= 10:
            return JsonResponse({'message': 'There are less than 10 transactions'})
        
        balance = int(await get_balance(address=address, api_key=api_key))/1000000
        anomaly_relation = await check_relation(address=address, api_key=api_key_chainalysis)

        if anomaly_relation['evaluation'] is True:
            return JsonResponse({'message': 'This address is on sanctions list', 'evaluation': 100})

        anomaly_value = await check_anomaly_value(transactions=transactions, minimum_threshold=TRON_SETTINGS['minimum_threshold'], maximum_threshold=TRON_SETTINGS['maximum_threshold'])
        anomaly_transfers = await check_anomaly_transfers(transactions=transactions, difference_time=TRON_SETTINGS['time_difference'], address=address)
        anomaly_hiding = await check_anomaly_hiding(transactions=transactions, address=address, time_difference=TRON_SETTINGS['time_difference'], api_key=api_key)

        finalEvaluation = get_finalEvaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient=TRON_SETTINGS['value_coefficient'], transfers_coefficient=TRON_SETTINGS['transfers_coefficient'], hiding_coefficient=TRON_SETTINGS['hiding_coefficient'], transactions_len=transactions_info['transactions_len'], balance=balance, first_transaction = transactions_info['first_transaction'], last_transaction = transactions_info['last_transaction'])
        
        return JsonResponse({'evaluation': finalEvaluation})

    response = inner()
    return response