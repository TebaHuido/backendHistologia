from rest_framework import serializers
from .models import Muestra

class MuestraSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    class Meta:
        model = Muestra
        fields = ['id', 'name','filename']
    def get_filename(self, obj):
        return obj.get_filename()