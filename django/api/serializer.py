from rest_framework import serializers
from .models import *
class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class AyudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayudante
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class SistemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sistema
        fields = '__all__'

class OrganoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organo
        fields = '__all__'
        
class CapturaSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Captura
        fields = ('id', 'name', 'image')  # Ajusta según tus necesidades

    def get_image(self, obj):
        relative_url = obj.image.url
        if relative_url.startswith('/muestras/'):
            relative_url = relative_url[len('/muestras/'):]
        server_url = 'http://localhost:80/images'
        full_url = f"{server_url}/{relative_url}"
        return full_url

class MuestraSerializer(serializers.ModelSerializer):
    images = CapturaSerializer(many=True)  # Para manejar las imágenes
    organo = OrganoSerializer(many=True)   # Relación ManyToMany con Organo
    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), many=True)

    class Meta:
        model = Muestra
        fields = ['id', 'name', 'categoria', 'organo', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        organo_data = validated_data.pop('organo')
        categoria_data = validated_data.pop('categoria')

        # Crear la muestra
        muestra = Muestra.objects.create(**validated_data)

        # Asociar las categorías
        muestra.categoria.set(categoria_data)

        # Crear y asociar los órganos
        for organo in organo_data:
            organo_instance = Organo.objects.create(**organo)
            muestra.organo.add(organo_instance)

        # Crear y asociar las imágenes
        for image_data in images_data:
            image_instance = Captura.objects.create(**image_data)
            muestra.images.add(image_instance)

        return muestra


class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'



class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notas
        fields = ('id', 'nota',)  # Ajusta según tus necesidades

class MuestraSerializer2(serializers.ModelSerializer):
    capturas = serializers.SerializerMethodField()
    notas = serializers.SerializerMethodField()
    sistemas = serializers.SerializerMethodField()

    class Meta:
        model = Muestra
        fields = ['id', 'name', 'capturas', 'notas', 'sistemas']

    def get_capturas(self, obj):
        capturas = obj.captura_set.all()
        return CapturaSerializer(capturas, many=True, context=self.context).data

    def get_notas(self, obj):
        notas = obj.notas_set.all()
        return NotaSerializer(notas, many=True).data

    def get_sistemas(self, obj):
        sistemas = obj.organo.all().values_list('sistema__name', flat=True)
        return list(sistemas) if sistemas else []

class TincionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tincion
        fields = '__all__'