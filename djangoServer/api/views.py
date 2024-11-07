# views.py

from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, status
from .models import *
from .serializer import *
from rest_framework.decorators import action
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import cv2
import os
from PIL import Image, PngImagePlugin
import uuid
from rest_framework.parsers import MultiPartParser, FormParser
import numpy as np
from django.http import FileResponse
from io import BytesIO


class ProcesarImagenAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # Verificar si se ha subido un archivo con la clave 'imagen'
        if 'imagen' not in request.FILES:
            return Response({"error": "No se ha subido ninguna imagen."}, status=status.HTTP_400_BAD_REQUEST)
        
        imagen = request.FILES['imagen']
        
        # Obtener parámetros de procesamiento desde el cuerpo de la solicitud o usar valores predeterminados
        scaleFactor = float(request.data.get('scaleFactor', 1.01))  # Valor predeterminado 1.01
        minNeighbors = int(request.data.get('minNeighbors', 5))     # Valor predeterminado 5
        minSize = tuple(map(int, request.data.get('minSize', '5,5').split(',')))  # Valor predeterminado (5, 5)
        maxSize = tuple(map(int, request.data.get('maxSize', '500,500').split(',')))  # Valor predeterminado (500, 500)
        shrink_factor = float(request.data.get('shrink_factor', 0.85))  # Valor predeterminado 0.85

        # Procesar la imagen y devolverla sin guardarla en el disco
        try:
            imagen_procesada, detecciones = self.procesar_imagen(
                imagen,
                scaleFactor=scaleFactor,
                minNeighbors=minNeighbors,
                minSize=minSize,
                maxSize=maxSize,
                shrink_factor=shrink_factor
            )
        except Exception as e:
            print(f"Error al procesar la imagen: {str(e)}")  # Depuración
            return Response({"error": f"Error al procesar la imagen: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Preparar la imagen para ser devuelta como respuesta
        response = FileResponse(imagen_procesada, content_type='image/png')
        response['Content-Disposition'] = 'inline; filename="imagen_procesada.png"'
        
        # Agregar detecciones en el cuerpo de la respuesta
        response['detecciones'] = detecciones
        
        return response

    def procesar_imagen(self, imagen_file, cascada_path=None, scaleFactor=1.01, minNeighbors=5, minSize=(5, 5), maxSize=(500,500), shrink_factor=0.85):
        # Verificar si el archivo de cascada existe
        if cascada_path is None:
            cascada_path = os.path.join(settings.BASE_DIR, 'api', 'cascades', 'cascade2.xml')
        
        if not os.path.exists(cascada_path):
            raise FileNotFoundError(f"El archivo de cascada no se encuentra en {cascada_path}")
        
        # Cargar el clasificador Haar Cascade
        cascada = cv2.CascadeClassifier(cascada_path)
        
        # Cargar la imagen desde el archivo en memoria
        imagen = cv2.imdecode(np.frombuffer(imagen_file.read(), np.uint8), cv2.IMREAD_COLOR)
        if imagen is None:
            raise ValueError("No se pudo cargar la imagen.")
        
        # Convertir a escala de grises para la detección
        gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        
        # Detectar objetos en la imagen
        objetos = cascada.detectMultiScale(
            gray, 
            scaleFactor=scaleFactor, 
            minNeighbors=minNeighbors, 
            minSize=minSize, 
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Filtrar objetos según el tamaño máximo, si se proporciona
        if maxSize is not None:
            max_width, max_height = maxSize
            objetos = [(x, y, w, h) for (x, y, w, h) in objetos if w <= max_width and h <= max_height]

        # Dibujar rectángulos más pequeños alrededor de los objetos detectados
        for (x, y, w, h) in objetos:
            new_w = int(w * shrink_factor)
            new_h = int(h * shrink_factor)
            new_x = x + (w - new_w) // 2
            new_y = y + (h - new_h) // 2
            cv2.rectangle(imagen, (new_x, new_y), (new_x + new_w, new_y + new_h), (255, 0, 0), 2)
        
        # Convertir la imagen a formato PNG en memoria
        _, buffer = cv2.imencode('.png', imagen)
        imagen_procesada = BytesIO(buffer)

        # Metadatos personalizados para las detecciones
        detecciones = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in objetos]
        
        # Retornar la imagen procesada y las detecciones
        return imagen_procesada, detecciones




class MuestraDetailAPIView(generics.RetrieveAPIView):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer2
    lookup_field = 'id'

class CapturaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer

class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return MuestraCreateSerializer  # Utilizamos el serializador de creación
        elif self.action == 'retrieve':
            return MuestraSerializer2  # Para detalles individuales
        else:
            return MuestraSerializer  # Para listar y otras acciones

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_name = request.query_params.get('category', None)

        if not categoria_name:
            return Response({"error": "Categoría no proporcionada"}, status=status.HTTP_400_BAD_REQUEST)

        if categoria_name == 'all':
            muestras = Muestra.objects.all()
        else:
            try:
                categoria = Categoria.objects.get(name=categoria_name)
                muestras = Muestra.objects.filter(Categoria=categoria)
            except Categoria.DoesNotExist:
                return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = MuestraSerializer(muestras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['request'] = request  # Para acceder a request.FILES si es necesario
        serializer.is_valid(raise_exception=True)
        muestra = serializer.save()
        return Response({'message': 'Muestra creada exitosamente'}, status=status.HTTP_201_CREATED)

def lista_capturas_muestra(request, muestra_id):
    muestra = get_object_or_404(Muestra, id=muestra_id)
    capturas = Captura.objects.filter(muestra=muestra)
    sistemas = muestra.organo.all().values_list('sistema__sisname', flat=True).distinct()
    organos = muestra.organo.all()
    categorias = muestra.Categoria.all()

    return render(request, 'lista_capturas_muestra.html', {
        'muestra': muestra,
        'capturas': capturas,
        'sistemas': sistemas,
        'organos': organos,
        'categorias': categorias
    })

def lista_imagenes(request):
    muestras = Muestra.objects.all()
    primeras_capturas = []

    for muestra in muestras:
        primera_captura = Captura.objects.filter(muestra=muestra).order_by('id').first()
        if primera_captura:
            primeras_capturas.append(primera_captura)

    return render(request, 'lista_imagenes.html', {'imagenes': primeras_capturas, 'muestras': muestras})

class ProfesorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class AyudanteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ayudante.objects.all()
    serializer_class = AyudanteSerializer

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SistemaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sistema.objects.all()
    serializer_class = SistemaSerializer

class OrganoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Organo.objects.all()
    serializer_class = OrganoSerializer

class LoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class AlumnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class NotasViewSet(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotaSerializer
