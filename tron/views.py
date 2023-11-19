from decouple import config
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse

from .serializers import StartResearchSerializer
from .commands.check_anomaly_hiding import check_anomaly_hiding
from .commands.check_anomaly_transfers import check_anomaly_transfers
from .commands.check_anomaly_value import check_anomaly_value
from .commands.check_relation import check_relation
from .commands.get_final_evaluation import get_final_evaluation
from .commands.get_transactions import get_transactions


api_key = config('API_TRONGRID_KEY')
api_key_chainalysis = config('CHAINALYSIS_API_KEY')

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

            transactions = get_transactions(address=address, api_key=api_key, params={'limit': 20})

            anomaly_value = check_anomaly_value(transactions=transactions, minimum_threshold=minimum_threshold, maximum_threshold=maximum_threshold)
            anomaly_transfers = check_anomaly_transfers(transactions=transactions, difference_time=time_difference, address=address)
            anomaly_hiding = check_anomaly_hiding(transactions=transactions, address=address, time_difference=time_difference)
            anomaly_relation = check_relation(address=address, api_key=api_key_chainalysis)

            final_evaluation = get_final_evaluation(anomaly_value, anomaly_transfers, anomaly_hiding, anomaly_relation, value_coefficient=value_coefficient, transfers_coefficient=transfers_coefficient, hiding_coefficient=hiding_coefficient, relation_coefficient=relation_coefficient)

            return JsonResponse({'evaluation': final_evaluation})

        return JsonResponse({'error': 'Invalid data'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)