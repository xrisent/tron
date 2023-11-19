from decouple import config
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import StartResearchSerializer
from .commands.check_anomaly_hiding import check_anomaly_hiding
from .commands.check_anomaly_transfers import check_anomaly_transfers
from .commands.check_anomaly_value import check_anomaly_value
from .commands.check_relation import check_relation
from .commands.get_final_evaluation import get_final_evaluation
from .commands.get_transactions import get_transactions
from .commands.get_account_balance import get_balance

api_key = config('API_TRONGRID_KEY')
api_key_chainalysis = config('CHAINALYSIS_API_KEY')

@swagger_auto_schema(
    methods=['post'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'minimum_threshold': openapi.Schema(type=openapi.TYPE_INTEGER),
            'maximum_threshold': openapi.Schema(type=openapi.TYPE_INTEGER),
            'time_difference': openapi.Schema(type=openapi.TYPE_INTEGER),
            'value_coefficient': openapi.Schema(type=openapi.TYPE_NUMBER),
            'transfers_coefficient': openapi.Schema(type=openapi.TYPE_NUMBER),
            'hiding_coefficient': openapi.Schema(type=openapi.TYPE_NUMBER),
            'relation_coefficient': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
        required=['address', 'minimum_threshold', 'maximum_threshold', 'time_difference', 'value_coefficient', 'transfers_coefficient', 'hiding_coefficient', 'relation_coefficient'],
    ),
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
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def start_research(request):
    if request.method == 'POST':
        serializer = StartResearchSerializer(data=request.data)
        if serializer.is_valid():
            address = serializer.validated_data['address']
            minimum_threshold = serializer.validated_data['minimum_threshold']
            maximum_threshold = serializer.validated_data['maximum_threshold']
            time_difference = serializer.validated_data['time_difference']
            value_coefficient = serializer.validated_data['value_coefficient']
            transfers_coefficient = serializer.validated_data['transfers_coefficient']
            hiding_coefficient = serializer.validated_data['hiding_coefficient']
            relation_coefficient = serializer.validated_data['relation_coefficient']

            try:
                transactions = get_transactions(address=address, api_key=api_key, params={'limit': 20})
            except:
                return JsonResponse({'error': 'Invalid address'})
            
            balance = int(get_balance(address=address, api_key=api_key))/1000000
            anomaly_value = check_anomaly_value(transactions=transactions, minimum_threshold=minimum_threshold, maximum_threshold=maximum_threshold)
            anomaly_transfers = check_anomaly_transfers(transactions=transactions, difference_time=time_difference, address=address)
            anomaly_hiding = check_anomaly_hiding(transactions=transactions, address=address, time_difference=time_difference, api_key=api_key)
            anomaly_relation = check_relation(address=address, api_key=api_key_chainalysis)

            final_evaluation = get_final_evaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient=value_coefficient, transfers_coefficient=transfers_coefficient, hiding_coefficient=hiding_coefficient, relation_coefficient=relation_coefficient, transactions_len=len(transactions), balance=balance)

            return JsonResponse({'evaluation': final_evaluation})

        return JsonResponse({'error': 'Invalid data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)