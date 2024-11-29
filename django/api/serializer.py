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
    #cd /usr/share/nginx/html
    image = serializers.SerializerMethodField()

    class Meta:
        model = Captura
        fields = ('id', 'name', 'image')  # Ajusta según tus necesidades

    def get_image(self, obj):
        relative_url = obj.image.url
        server_url = 'http://localhost:80'
        full_url = f"{server_url}{relative_url}"
        return full_url



class MuestraSerializer(serializers.ModelSerializer):
    imagenUrl = serializers.SerializerMethodField()  # Para incluir la URL de la imagen
    categoria = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True  # Solo se usará para crear
    )
    organo = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True  # Solo se usará para crear
    )
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True  # Solo para crear
    )
    sistema = serializers.SerializerMethodField()  # Campo para los sistemas asociados

    class Meta:
        model = Muestra
        fields = ['id', 'name', 'categoria', 'organo', 'sistema', 'images', 'imagenUrl']

    def validate_categoria(self, value):
        """
        Validamos las categorías, creando si no existen.
        """
        categorias = []
        for name in value:
            name_normalized = name.strip().lower()  # Normaliza los nombres
            categoria, _ = Categoria.objects.get_or_create(name=name_normalized)
            categorias.append(categoria)
        return categorias

    def validate_organo(self, value):
        """
        Validamos los órganos, creando si no existen.
        """
        organos = []
        for name in value:
            name_normalized = name.strip().lower()  # Normaliza los nombres
            organo, _ = Organo.objects.get_or_create(name=name_normalized)
            organos.append(organo)
        return organos

    def create(self, validated_data):
        """
        Creamos la muestra, asignando categorías, órganos, sistemas e imágenes.
        """
        categoria_instances = validated_data.pop('categoria')
        organo_instances = validated_data.pop('organo')
        images = validated_data.pop('images')

        # Creamos la muestra
        muestra = Muestra.objects.create(**validated_data)

        # Asociamos categorías y órganos a la muestra
        muestra.Categoria.set(categoria_instances)
        muestra.organo.set(organo_instances)

        # Asociamos los sistemas de los órganos a la muestra
        sistemas = set()
        for organo in organo_instances:
            sistemas.update(organo.sistema.all())  # Extrae todos los sistemas asociados

        # Si `sistemas` es una relación directa de `Muestra`
        if hasattr(muestra, 'sistemas'):
            muestra.sistemas.set(sistemas)

        # Creamos las capturas asociadas
        for image in images:
            Captura.objects.create(image=image, muestra=muestra)

        return muestra

    def get_imagenUrl(self, obj):
        """
        Obtenemos la URL de la primera captura asociada a la muestra.
        """
        captura = obj.captura_set.first()  # Obtiene la primera captura asociada
        if captura:
            return captura.image.url
        return None

    def get_sistema(self, obj):
        """
        Obtenemos los sistemas relacionados con los órganos de la muestra.
        """
        sistemas = set()
        for organo in obj.organo.all():
            sistemas.update(organo.sistema.values_list('name', flat=True))
        return list(sistemas)

    def get_imagenUrl(self, obj):
        """
        Obtenemos la URL de la primera captura asociada a la muestra.
        """
        captura = obj.captura_set.first()  # Obtiene la primera captura asociada
        if captura:
            return captura.image.url
        return None

    def get_sistema(self, obj):
        """
        Obtenemos los sistemas de los órganos asociados a la muestra.
        """
        sistemas = set()
        for organo in obj.organo.all():
            if organo.sistema:
                sistemas.add(organo.sistema.name)  # Asegúrate de acceder al nombre del sistema
        return list(sistemas)


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