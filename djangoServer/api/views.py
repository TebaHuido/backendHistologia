from rest_framework import viewsets
from .serializer import MuestraSerializer
from .models import Muestra

# Create your views here.
class MuestraViewSet(viewsets.ModelViewSet):
    queryset = Muestra.objects.all()
    serializer_class = MuestraSerializer