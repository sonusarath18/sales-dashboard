from rest_framework import serializers
from .models import Expense

class SalesRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
