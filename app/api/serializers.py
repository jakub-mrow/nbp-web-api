from rest_framework import serializers
from api.models import Currencies

class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = '__all__'