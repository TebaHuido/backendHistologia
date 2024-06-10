from django.shortcuts import render
from rest_framework import viewsets
from .serializer import MuestraSerializer
from .models import Muestra
from django.http import HttpResponse

# Create your views here.
class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer


def lista_imagenes(request):
    imagenes = Muestra.objects.all()
    return render(request, 'lista_imagenes.html', {'imagenes': imagenes})