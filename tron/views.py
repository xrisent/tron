from decouple import config
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .commands.check_anomaly_hiding import check_anomaly_hiding
from .commands.check_anomaly_transfers import check_anomaly_transfers
from .commands.check_anomaly_value import check_anomaly_value
from .commands.check_relation import check_relation
from .commands.get_finalEvaluation import get_finalEvaluation
from .commands.get_transactions import get_transactions
from .commands.get_account_balance import get_balance
# from .commands.get_transactions_len import get_len

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

    try:
        transactions = get_transactions(address=address, api_key=api_key, params=TRON_SETTINGS['params'])
    except:
        return JsonResponse({'error': 'Invalid address'})
    
    balance = int(get_balance(address=address, api_key=api_key))/1000000
    anomaly_value = check_anomaly_value(transactions=transactions, minimum_threshold=TRON_SETTINGS['minimum_threshold'], maximum_threshold=TRON_SETTINGS['maximum_threshold'])
    anomaly_transfers = check_anomaly_transfers(transactions=transactions, difference_time=TRON_SETTINGS['time_difference'], address=address)
    anomaly_hiding = check_anomaly_hiding(transactions=transactions, address=address, time_difference=TRON_SETTINGS['time_difference'], api_key=api_key)
    anomaly_relation = check_relation(address=address, api_key=api_key_chainalysis)

    finalEvaluation = get_finalEvaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient=TRON_SETTINGS['value_coefficient'], transfers_coefficient=TRON_SETTINGS['transfers_coefficient'], hiding_coefficient=TRON_SETTINGS['hiding_coefficient'], relation_coefficient=TRON_SETTINGS['relation_coefficient'], transactions_len=len(transactions), balance=balance)

# transactions_len=get_len(address=address, api_key=api_key)

    return JsonResponse({'evaluation': finalEvaluation})