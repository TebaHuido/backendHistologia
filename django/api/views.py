# Importa herramientas de Django para manejar vistas y recuperar objetos
from django.shortcuts import render, get_object_or_404
import json
from rest_framework.views import APIView
# Importa módulos de DRF (Django Rest Framework) para crear API y vistas
from rest_framework import viewsets, generics ,status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# Importa los modelos que serán utilizados en las vistas
from .models import (
    Profesor, Curso, Ayudante, Categoria, Sistema, Organo, 
    Muestra, Lote, Alumno, Captura, Notas, Tag, Tincion, CustomUser
)

# Importa los serializers para transformar los datos en formatos adecuados para la API
from .serializer import (
    MuestraSerializer2, NotaSerializer, CapturaSerializer, ProfesorSerializer, 
    CursoSerializer, AyudanteSerializer, CategoriaSerializer, SistemaSerializer, 
    OrganoSerializer, MuestraSerializer, LoteSerializer, AlumnoSerializer,
    TincionSerializer, TagsSerializer, UserSerializer, ProfesorCreateSerializer
)

from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsProfesor

import logging
import sys
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware.csrf import get_token
from django.http import JsonResponse
from .utils import create_alumnos_from_xls  # Ensure this import is present

logger = logging.getLogger(__name__)

# Redirige los mensajes print a stdout
sys.stdout = sys.stderr

# Vista genérica para recuperar el detalle de una muestra específica por ID
class FilterView(APIView):
    def get(self, request, *args, **kwargs):
        categorias_serializadas = CategoriaSerializer(Categoria.objects.all(), many=True).data
        organos_serializados = OrganoSerializer(Organo.objects.all(), many=True).data
        sistemas_serializados = SistemaSerializer(Sistema.objects.all(), many=True).data
        tinciones_serializadas = TincionSerializer(Tincion.objects.all(), many=True).data
        tags_serializados = TagsSerializer(Tag.objects.all(), many=True).data

        return Response({
            "categorias": categorias_serializadas,
            "organos": organos_serializados,
            "sistemas": sistemas_serializados,
            "tinciones": tinciones_serializadas,
            "tags": tags_serializados
        })

class MuestraDetailAPIView(generics.RetrieveAPIView):
    # Define el conjunto de datos que consulta
    queryset = Muestra.objects.all()
    # Usa el serializer correspondiente para estructurar los datos
    serializer_class = MuestraSerializer2
    # Indica que el parámetro usado para buscar es el ID
    lookup_field = 'id'

# Vista para manejar capturas (solo lectura)
class CapturaViewSet(viewsets.ReadOnlyModelViewSet):
    # Define el conjunto de datos y el serializer para el modelo Captura
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer


class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)

        # Devolver la respuesta con los datos creados
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    @action(detail=False, methods=['get'])
    
    def Filtrado(self, request):
        categories = request.query_params.getlist('category', [])
        organs = request.query_params.getlist('organ', [])
        systems = request.query_params.getlist('system', [])
        tincions = request.query_params.getlist('tincion', [])
        tags = request.query_params.getlist('tag', [])

        muestras = Muestra.objects.all()

        if categories:
            muestras = muestras.filter(Categoria__name__in=categories)
        if organs:
            muestras = muestras.filter(organo__name__in=organs)
        if systems:
            muestras = muestras.filter(organo__sistema__name__in=systems)
        if tincions:
            muestras = muestras.filter(tincion__name__in=tincions)
        if tags:
            muestras = muestras.filter(notas__tags__name__in=tags)

        serializer = MuestraSerializer(muestras.distinct(), many=True)
        return Response(serializer.data)
# Función para listar capturas asociadas a una muestra específica
def lista_capturas_muestra(request, muestra_id):
    # Recupera la muestra o lanza un error si no existe
    muestra = get_object_or_404(Muestra, id=muestra_id)
    # Recupera las capturas asociadas a la muestra
    capturas = Captura.objects.filter(muestra=muestra)
    # Recupera los sistemas y órganos relacionados con la muestra
    sistemas = muestra.organo.all().values_list('sistema__name', flat=True).distinct()
    organos = muestra.organo.all()
    categorias = muestra.Categoria.all()

    # Renderiza la plantilla HTML con los datos
    return render(request, 'lista_capturas_muestra.html', {
        'muestra': muestra,
        'capturas': capturas,
        'sistemas': sistemas,
        'organos': organos,
        'categorias': categorias
    })

# Función para listar todas las imágenes disponibles (primera captura de cada muestra)
def lista_imagenes(request):
    # Recupera todas las muestras
    muestras = Muestra.objects.all()
    primeras_capturas = []

    # Busca la primera captura de cada muestra
    for muestra in muestras:
        primera_captura = Captura.objects.filter(muestra=muestra).order_by('id').first()
        if primera_captura:
            primeras_capturas.append(primera_captura)

    # Renderiza la plantilla HTML con las imágenes destacadas
    return render(request, 'lista_imagenes.html', {
        'imagenes': primeras_capturas,
        'muestras': muestras
    })

# Vista para manejar profesores (solo lectura)
class ProfesorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

# Vista para manejar cursos (solo lectura)
class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

# Vista para manejar ayudantes (solo lectura)
class AyudanteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ayudante.objects.all()
    serializer_class = AyudanteSerializer

# Vista para manejar categorías (solo lectura)
class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# Vista para manejar sistemas (solo lectura)
class SistemaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sistema.objects.all()
    serializer_class = SistemaSerializer

# Vista para manejar órganos (solo lectura)
class OrganoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organo.objects.all()
    serializer_class = OrganoSerializer

# Vista alternativa para manejar muestras (solo lectura)
class MuestraViewSet2(viewsets.ReadOnlyModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer

# Vista para manejar lotes (solo lectura)
class LoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

# Vista para manejar alumnos (solo lectura)
class AlumnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

# Vista para manejar capturas (solo lectura, duplicada para énfasis)
class CapturaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer

# Vista para manejar notas (CRUD completo)
class NotaViewSet(viewsets.ModelViewSet):
    queryset = Notas.objects.all().select_related('alumno', 'profesor', 'muestra').prefetch_related('tags')
    serializer_class = NotaSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_alumno:
            serializer.save(alumno=user)
        elif user.is_profesor:
            serializer.save(profesor=user)
        else:
            raise serializers.ValidationError("User must be either an alumno or a profesor")

    def create(self, request, *args, **kwargs):
        data = request.data.get('nota', {})  # Ensure the data is wrapped in a 'nota' key
        user = request.user

        if user.is_alumno:
            data['alumno'] = user.id
        elif user.is_profesor:
            data['profesor'] = user.id
        else:
            return Response({'error': 'User must be either an alumno or a profesor'}, status=status.HTTP_400_BAD_REQUEST)

        # Desempaqueta los datos de la nota
        nota_data = {
            'titulo': data.get('titulo', ''),
            'cuerpo': data.get('cuerpo', ''),
            'alumno': data.get('alumno'),
            'profesor': data.get('profesor'),
            'muestra': data.get('muestra')
        }

        serializer = self.get_serializer(data=nota_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.get('nota', {})  # Ensure the data is wrapped in a 'nota' key

        # Desempaqueta los datos de la nota
        nota_data = {
            'titulo': data.get('titulo', ''),
            'cuerpo': data.get('cuerpo', ''),
            'alumno': data.get('alumno'),
            'profesor': data.get('profesor'),
            'muestra': data.get('muestra')
        }

        serializer = self.get_serializer(instance, data=nota_data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        if user.is_alumno:
            return Notas.objects.filter(alumno=user).select_related('alumno', 'profesor', 'muestra').prefetch_related('tags')
        elif user.is_profesor:
            return Notas.objects.filter(profesor=user).select_related('alumno', 'profesor', 'muestra').prefetch_related('tags')
        return Notas.objects.none()

class TincionViewSet(viewsets.ModelViewSet):
    queryset = Tincion.objects.all()
    serializer_class = TincionSerializer

class MuestraFilterAPIView(generics.ListAPIView):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        categoria_id = self.request.query_params.get('categoria')
        sistema_id = self.request.query_params.get('sistema')
        organo_id = self.request.query_params.get('organo')
        tincion_id = self.request.query_params.get('tincion')
        tag_id = self.request.query_params.get('tag')

        if categoria_id:
            queryset = queryset.filter(Categoria__id=categoria_id)
        if sistema_id:
            queryset = queryset.filter(organo__sistema__id=sistema_id)
        if organo_id:
            queryset = queryset.filter(organo__id=organo_id)
        if tincion_id:
            queryset = queryset.filter(tincion__id=tincion_id)
        if tag_id:
            queryset = queryset.filter(notas__tags__id=tag_id)

        return queryset.distinct()
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to access this view

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                user_data = UserSerializer(user).data
                csrf_token = get_token(request)
                response = JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': user_data
                })
                response.set_cookie('csrftoken', csrf_token, httponly=True)  # Ensure CSRF token is set in cookies
                return response
            else:
                return Response({'error': 'User account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfesorCreateView(generics.CreateAPIView):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorCreateSerializer

class UplimageView(APIView):
    permission_classes = [IsAuthenticated, IsProfesor]

    def post(self, request, *args, **kwargs):
        # Lógica para manejar la subida de imágenes
        pass

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class UploadXlsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            try:
                result = create_alumnos_from_xls(file)
                csrf_token = get_token(request)
                response = Response({
                    "message": "File processed successfully",
                    "curso": result["curso"],
                    "curso_created": result["curso_created"],
                    "created_alumnos": result["created_alumnos"],
                    "existing_alumnos": result["existing_alumnos"]
                }, status=status.HTTP_200_OK)
                response.set_cookie('csrftoken', csrf_token, httponly=True)
                return response
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)