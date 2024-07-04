from django.urls import path, include
from rest_framework import routers
from api import views
from api.views import lista_imagenes
router = routers.DefaultRouter()
router.register(r'muestra', views.CapturaViewSet)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'ayudantes', views.AyudanteViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'sistemas', views.SistemaViewSet)
router.register(r'organos', views.OrganoViewSet)
router.register(r'muestras', views.MuestraViewSet)
router.register(r'lotes', views.LoteViewSet)
router.register(r'alumnos', views.AlumnoViewSet)
router.register(r'capturas', views.CapturaViewSet)

urlpatterns = [
    path('imagenes/', views.lista_imagenes, name='lista_imagenes'),
    path('', include(router.urls)),
]
