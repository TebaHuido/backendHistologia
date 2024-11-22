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
router.register(r'notas', views.NotasViewSet)
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'ayudantes', views.AyudanteViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'sistemas', views.SistemaViewSet)
router.register(r'organos', views.OrganoViewSet)
router.register(r'muestras', views.MuestraViewSet, basename='muestra')  # Nombre base 'muestra'
router.register(r'muestrass', views.MuestraViewSet2, basename='muestra2')  # Nombre base 'muestra2'
router.register(r'lotes', views.LoteViewSet)
router.register(r'alumnos', views.AlumnoViewSet)
router.register(r'capturas', views.CapturaViewSet)
router.register(r'tinciones', views.TincionViewSet)

urlpatterns = [
    path('muestra3/<int:id>/', views.MuestraDetailAPIView.as_view(), name='muestra-detail'),
    path('imagenes/', views.lista_imagenes, name='lista_imagenes'),#vista tipo frontend
    path('muestras/por_categoria/', views.MuestraViewSet.as_view({'get': 'por_categoria'}), name='muestras_por_categoria'),
    path('lista_capturas_muestra/<int:muestra_id>/', views.lista_capturas_muestra, name='lista_capturas_muestra'),#vista tipo frontend
    path('', include(router.urls)),
]
