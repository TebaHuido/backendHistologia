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

class ProcesarImagenAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # Depuración: Imprimir archivos recibidos
        print("Archivos recibidos:", request.FILES)

        # Verificar si se ha subido un archivo con la clave 'imagen'
        if 'imagen' not in request.FILES:
            return Response({"error": "No se ha subido ninguna imagen."}, status=status.HTTP_400_BAD_REQUEST)
        
        imagen = request.FILES['imagen']
        
        # Guardar la imagen original en una ubicación temporal
        nombre_unico = f"{uuid.uuid4()}_{imagen.name}"
        ruta_original = os.path.join(settings.MEDIA_ROOT, 'originales', nombre_unico)
        
        # Asegurarse de que el directorio existe
        os.makedirs(os.path.dirname(ruta_original), exist_ok=True)
        
        # Guardar la imagen
        with open(ruta_original, 'wb+') as destino:
            for chunk in imagen.chunks():
                destino.write(chunk)
        
        # Procesar la imagen con Haar Cascade
        try:
            ruta_procesada, detecciones = self.procesar_imagen(ruta_original)
        except Exception as e:
            # Eliminar la imagen original en caso de error
            os.remove(ruta_original)
            print(f"Error al procesar la imagen: {str(e)}")  # Depuración
            return Response({"error": f"Error al procesar la imagen: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Generar la URL pública de la imagen procesada
        url_procesada = request.build_absolute_uri(settings.MEDIA_URL + ruta_procesada)
        
        # Retornar la URL y los metadatos de detección
        response_data = {
            "imagen_original": request.build_absolute_uri(settings.MEDIA_URL + 'originales/' + nombre_unico),
            "imagen_procesada": url_procesada,
            "metadata": detecciones
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    def procesar_imagen(self, imagen_path, cascada_path=None, scaleFactor=1.07, minNeighbors=15, minSize=(15, 15), shrink_factor=0.85):
        # Verificar si el archivo de cascada existe
        if cascada_path is None:
            cascada_path = os.path.join(settings.BASE_DIR, 'api', 'cascades', 'cascade2.xml')
        
        if not os.path.exists(cascada_path):
            raise FileNotFoundError(f"El archivo de cascada no se encuentra en {cascada_path}")
        
        # Cargar el clasificador Haar Cascade
        cascada = cv2.CascadeClassifier(cascada_path)
        
        # Cargar la imagen
        imagen = cv2.imread(imagen_path)
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
        
        # Dibujar rectángulos más pequeños alrededor de los objetos detectados
        for (x, y, w, h) in objetos:
            new_w = int(w * shrink_factor)
            new_h = int(h * shrink_factor)
            new_x = x + (w - new_w) // 2
            new_y = y + (h - new_h) // 2
            cv2.rectangle(imagen, (new_x, new_y), (new_x + new_w, new_y + new_h), (255, 0, 0), 2)
        
        # Generar un nombre de archivo único para la imagen procesada
        nombre_unico = f"{uuid.uuid4()}.png"
        
        # Guardar la imagen procesada con OpenCV
        cv2.imwrite(nombre_unico, imagen)
        
        # Metadatos personalizados
        detecciones = [{
            "x": int(x),
            "y": int(y),
            "w": int(w),
            "h": int(h)
        } for (x, y, w, h) in objetos]
        
        # Retornar la ruta relativa y las detecciones
        return nombre_unico, detecciones


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
