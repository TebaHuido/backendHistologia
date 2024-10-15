# serializers.py

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
    class Meta:
        model = Captura
        fields = ('id', 'name', 'image', 'muestra_id', 'aumento')

class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notas
        fields = ('id', 'nota',)

class MuestraSerializer(serializers.ModelSerializer):
    imagenUrl = serializers.SerializerMethodField()
    sistema = serializers.SerializerMethodField()

    class Meta:
        model = Muestra
        fields = ['id', 'name', 'imagenUrl', 'sistema']

    def get_imagenUrl(self, obj):
        first_image = obj.captura_set.first()
        if first_image:
            # Obtener la URL relativa de la imagen
            relative_url = first_image.image.url  # Ejemplo: 'muestras/a9e929b1-5acb-404d-8798-329166b222d4.gif'
            
            # Eliminar la parte '/muestras' de la URL relativa
            if relative_url.startswith('/muestras/'):
                relative_url = relative_url[len('/muestras/'):]  # Elimina 'muestras/' del inicio
            
            # Construir manualmente la URL completa
            server_url = 'http://localhost:8011/images'  # Ajusta el dominio y puerto según tu configuración
            full_url = f"{server_url}/{relative_url}"  # Combina el dominio con la URL relativa corregida
            return full_url
        return None

    def get_sistema(self, obj):
        sistemas = obj.organo.all().values_list('sistema__sisname', flat=True)
        if sistemas:
            return sistemas[0]  # Devuelve el primer sistema asociado
        return None

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
        sistemas = obj.organo.all().values_list('sistema__sisname', flat=True)
        return list(sistemas) if sistemas else []

class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumno
        fields = '__all__'

# serializers.py

class MuestraCreateSerializer(serializers.ModelSerializer):
    Categoria = serializers.IntegerField(write_only=True, required=False)
    new_category = serializers.CharField(write_only=True, required=False)
    Organo = serializers.IntegerField(write_only=True, required=False)
    new_organo = serializers.CharField(write_only=True, required=False)
    new_sistema = serializers.CharField(write_only=True, required=False)
    Sistema = serializers.IntegerField(write_only=True, required=False)
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    image_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Muestra
        fields = [
            'id', 'name', 'Categoria', 'new_category',
            'Organo', 'new_organo', 'Sistema', 'new_sistema',
            'images', 'image_names'
        ]

    def create(self, validated_data):
        name = validated_data.get('name')
        category_id = validated_data.pop('Categoria', None)
        new_category_name = validated_data.pop('new_category', None)
        organo_id = validated_data.pop('Organo', None)
        new_organo_name = validated_data.pop('new_organo', None)
        sistema_id = validated_data.pop('Sistema', None)
        new_sistema_name = validated_data.pop('new_sistema', None)
        images = validated_data.pop('images', [])
        image_names = validated_data.pop('image_names', [])

        # Crear la muestra
        muestra = Muestra.objects.create(name=name)

        # Manejar categoría existente
        if category_id:
            try:
                category = Categoria.objects.get(id=category_id)
                muestra.Categoria.add(category)
            except Categoria.DoesNotExist:
                raise serializers.ValidationError({'Categoria': 'La categoría no existe.'})

        # Crear nueva categoría si se proporciona
        if new_category_name:
            new_category, created = Categoria.objects.get_or_create(name=new_category_name)
            muestra.Categoria.add(new_category)

        # Manejar órgano existente
        if organo_id:
            try:
                organo = Organo.objects.get(id=organo_id)
                muestra.organo.add(organo)
            except Organo.DoesNotExist:
                raise serializers.ValidationError({'Organo': 'El órgano no existe.'})

        # Crear nuevo órgano si se proporciona
        if new_organo_name:
            # Crear nuevo órgano
            new_organo = Organo.objects.create(orgname=new_organo_name)

            # Manejar sistema para el nuevo órgano
            if sistema_id:
                try:
                    sistema = Sistema.objects.get(id=sistema_id)
                    new_organo.sistema.add(new_sistema)
                except Sistema.DoesNotExist:
                    raise serializers.ValidationError({'Sistema': 'El sistema no existe.'})
            elif new_sistema_name:
                # Crear nuevo sistema y asignarlo al órgano
                new_sistema, created = Sistema.objects.get_or_create(sisname=new_sistema_name)
                new_organo.sistema.add(new_sistema)

            new_organo.save()
            muestra.organo.add(new_organo)

        # Manejar las capturas (imágenes)
        for i, image in enumerate(images):
            image_name = image_names[i] if i < len(image_names) else f"Imagen {i+1}"
            Captura.objects.create(
                name=image_name,
                image=image,
                muestra=muestra
            )

        return muestra
