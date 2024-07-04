from django.shortcuts import render
from rest_framework import viewsets
from .models import Profesor, Curso, Ayudante, Categoria, Sistema, Organo, Muestra, Lote, Alumno, Captura
from .serializer import CapturaSerializer, ProfesorSerializer, CursoSerializer, AyudanteSerializer, CategoriaSerializer, SistemaSerializer, OrganoSerializer, MuestraSerializer, LoteSerializer, AlumnoSerializer, CapturaSerializer

# Create your views here.
class CapturaViewSet(viewsets.ModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer


def lista_imagenes(request):
    imagenes = Captura.objects.all()
    return render(request, 'lista_imagenes.html', {'imagenes': imagenes})
# En tu aplicación Django, por ejemplo, 'api_app/views.py'
class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class AyudanteViewSet(viewsets.ModelViewSet):
    queryset = Ayudante.objects.all()
    serializer_class = AyudanteSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class SistemaViewSet(viewsets.ModelViewSet):
    queryset = Sistema.objects.all()
    serializer_class = SistemaSerializer

class OrganoViewSet(viewsets.ModelViewSet):
    queryset = Organo.objects.all()
    serializer_class = OrganoSerializer

class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer

class CapturaViewSet(viewsets.ModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer
