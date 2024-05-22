from rest_framework.serializers import ModelSerializer
from myapp.models import Journey
import json

class JourneySerializer(ModelSerializer):
    class Meta:
        model = Journey
        fields = '__all__'
        