from rest_framework.serializers import ModelSerializer
from myapp.models import Place
import json

class placeSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
        