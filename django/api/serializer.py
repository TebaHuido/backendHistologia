from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'is_alumno', 'is_profesor', 'password']

class ProfesorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profesor
        fields = '__all__'

class ProfesorCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profesor
        fields = ['user', 'name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = CustomUser(**user_data)
        user.set_password(password)
        user.is_profesor = True
        user.save()
        profesor = Profesor.objects.create(user=user, **validated_data)
        print(f"Created user: {user.username} with password: {password}")  # Mensaje de depuración
        return profesor

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
    sistema = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True  # Solo se usará para crear
    )
    tincion = serializers.ListField(
        child=serializers.CharField(max_length=100),
        write_only=True  # Solo se usará para crear
    )
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True  # Solo para crear
    )

    class Meta:
        model = Muestra
        fields = ['id', 'name', 'categoria', 'organo', 'sistema', 'tincion', 'images', 'imagenUrl']

    def validate_categoria(self, value):
        categorias = []
        for name in value:
            name_normalized = name.strip().lower()
            categoria, _ = Categoria.objects.get_or_create(name=name_normalized)
            categorias.append(categoria)
        return categorias

    def validate_organo(self, value):
        organos = []
        for name in value:
            name_normalized = name.strip().lower()
            organo, _ = Organo.objects.get_or_create(name=name_normalized)
            organos.append(organo)
        return organos

    def validate_sistema(self, value):
        sistemas = []
        for name in value:
            name_normalized = name.strip().lower()
            sistema, _ = Sistema.objects.get_or_create(name=name_normalized)
            sistemas.append(sistema)
        return sistemas

    def validate_tincion(self, value):
        tinciones = []
        for name in value:
            name_normalized = name.strip().lower()
            tincion, _ = Tincion.objects.get_or_create(name=name_normalized)
            tinciones.append(tincion)
        return tinciones

    def create(self, validated_data):
        categoria_instances = validated_data.pop('categoria')
        organo_instances = validated_data.pop('organo')
        sistema_instances = validated_data.pop('sistema', [])
        tincion_instances = validated_data.pop('tincion')
        images = validated_data.pop('images')

        # Creamos la muestra
        muestra = Muestra.objects.create(**validated_data)

        # Asociamos categorías, órganos, sistemas y tinciones
        muestra.Categoria.set(categoria_instances)
        muestra.organo.set(organo_instances)
        muestra.tincion.set(tincion_instances)

        # Solo asociamos sistemas si se han proporcionado
        if sistema_instances and sistema_instances != 'null':
            for organo in organo_instances:
                if isinstance(organo, Organo):
                    organo.sistema.set(sistema_instances)
                else:
                    organo_obj = Organo.objects.get(name=organo.name)
                    organo_obj.sistema.set(sistema_instances)

        # Asociamos las imágenes a las capturas
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

    def get_sistemas(self, obj):
        organos = obj.organo.all()
        sistemas = []
        for organo in organos:
            for sistema in organo.sistema.all():
                sistemas.append({'sistema': sistema.name, 'organo': organo.name})
        return sistemas if sistemas else []



class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

class AlumnoSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Alumno
        fields = ['user', 'name', 'curso', 'permiso']

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
        organos = obj.organo.all()
        sistemas = []
        for organo in organos:
            for sistema in organo.sistema.all():
                sistemas.append({'sistema': sistema.name, 'organo': organo.name})
        return sistemas if sistemas else []

class TincionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tincion
        fields = '__all__'
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'