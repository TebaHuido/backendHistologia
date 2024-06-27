from rest_framework import serializers
from .models import Captura

class CapturaSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = Captura
        fields = ['id', 'name','filename']
    def get_filename(self, obj):
        return obj.get_filename()