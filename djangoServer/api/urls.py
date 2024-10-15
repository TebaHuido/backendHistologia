# urls.py

from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'notas', views.NotasViewSet)
router.register(r'profesores', views.ProfesorViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'ayudantes', views.AyudanteViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'sistemas', views.SistemaViewSet)
router.register(r'organos', views.OrganoViewSet)
router.register(r'muestras', views.MuestraViewSet, basename='muestras')
router.register(r'lotes', views.LoteViewSet)
router.register(r'alumnos', views.AlumnoViewSet)
router.register(r'capturas', views.CapturaViewSet)

urlpatterns = [
    path('procesar-imagen/', views.ProcesarImagenAPIView.as_view(), name='procesar-imagen'),
    path('muestra3/<int:id>/', views.MuestraDetailAPIView.as_view(), name='muestra-detail'),
    path('imagenes/', views.lista_imagenes, name='lista_imagenes'),
    path('muestras/por_categoria/', views.MuestraViewSet.as_view({'get': 'por_categoria'}), name='muestras_por_categoria'),
    path('lista_capturas_muestra/<int:muestra_id>/', views.lista_capturas_muestra, name='lista_capturas_muestra'),
    path('', include(router.urls)),
]
