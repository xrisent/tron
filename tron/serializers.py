from rest_framework import serializers

class StartResearchSerializer(serializers.Serializer):
    address = serializers.CharField()
    threshold = serializers.IntegerField()
    time_difference = serializers.IntegerField()