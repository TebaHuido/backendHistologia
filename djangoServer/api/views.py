from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets
from .models import Profesor, Curso, Ayudante, Categoria, Sistema, Organo, Muestra, Lote, Alumno, Captura,Notas
from .serializer import MuestraSerializer2,NotaSerializer, CapturaSerializer, ProfesorSerializer, CursoSerializer, AyudanteSerializer, CategoriaSerializer, SistemaSerializer, OrganoSerializer, MuestraSerializer, LoteSerializer, AlumnoSerializer, CapturaSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.http import JsonResponse
# Create your views here.
from rest_framework import viewsets


class MuestraDetailAPIView(generics.RetrieveAPIView):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer2
    lookup_field = 'id'

class CapturaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer
class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer
    parser_classes = (MultiPartParser, FormParser)
    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_name = request.query_params.get('category', None)

        if not categoria_name:
            return Response({"error": "Categoría no proporcionada"}, status=status.HTTP_400_BAD_REQUEST)

        # Caso especial para devolver todas las muestras sin filtrar
        if categoria_name == 'all':
            muestras = Muestra.objects.all()
            serializer = self.get_serializer(muestras, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Manejo del resto de las categorías
        try:
            categoria = Categoria.objects.get(name=categoria_name)
            muestras = Muestra.objects.filter(Categoria=categoria)
        except Categoria.DoesNotExist:
            return Response({"error": "Categoría no encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(muestras, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    return render(request, 'lista_imagenes.html', {'imagenes': primeras_capturas,'muestras': muestras})
# En tu aplicación Django, por ejemplo, 'api_app/views.py'
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

class MuestraViewSet2(viewsets.ReadOnlyModelViewSet):
    def post(self, request, *args, **kwargs):
        # Tu lógica aquí
        return JsonResponse({'status': 'success'})
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer

class LoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class AlumnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CapturaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer
class NotasViewSet(viewsets.ModelViewSet):
    queryset = Notas.objects.all()
    serializer_class = NotaSerializer