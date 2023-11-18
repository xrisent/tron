from rest_framework import serializers

class StartResearchSerializer(serializers.Serializer):
    address = serializers.CharField()
    minimum_threshold = serializers.IntegerField()
    maximum_threshold = serializers.IntegerField()
    time_difference = serializers.IntegerField()
    value_coefficient = serializers.FloatField()
    transfers_coefficient = serializers.FloatField()
    hiding_coefficient = serializers.FloatField()
    relation_coefficient = serializers.FloatField()