from rest_framework import serializers
from .models import  Wishmodel

class Wishserializer(serializers.ModelSerializer):
    class Meta:
        model = Wishmodel
        fields = ('id', 'text', 'to_number', "audio", "date_of_send", "voise", "status", 'tarif')
        read_only_fields = ('author',)


class TextSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=1000)
    class Meta:
        model=Wishmodel
        fields=('text',)
