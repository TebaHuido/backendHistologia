from django.shortcuts import render
from rest_framework import viewsets
from .serializer import CapturaSerializer
from .models import Captura
from django.http import HttpResponse

# Create your views here.
class CapturaViewSet(viewsets.ModelViewSet):
    queryset = Captura.objects.all()
    serializer_class = CapturaSerializer


def lista_imagenes(request):
    imagenes = Captura.objects.all()
    return render(request, 'lista_imagenes.html', {'imagenes': imagenes})