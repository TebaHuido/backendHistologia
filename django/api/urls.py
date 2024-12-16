from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from .views import LoginView

router = DefaultRouter()
router.register(r'notas', views.NotasViewSet, basename='notas')
router.register(r'profesores', views.ProfesorViewSet, basename='profesores')
router.register(r'cursos', views.CursoViewSet, basename='cursos')
router.register(r'ayudantes', views.AyudanteViewSet, basename='ayudantes')
router.register(r'categorias', views.CategoriaViewSet, basename='categorias')
router.register(r'sistemas', views.SistemaViewSet, basename='sistemas')
router.register(r'organos', views.OrganoViewSet, basename='organos')
router.register(r'muestras', views.MuestraViewSet, basename='muestras')
router.register(r'muestra_alt', views.MuestraViewSet2, basename='muestra2')
router.register(r'lotes', views.LoteViewSet, basename='lotes')
router.register(r'alumnos', views.AlumnoViewSet, basename='alumnos')
router.register(r'tinciones', views.TincionViewSet, basename='tinciones')

urlpatterns = [
    path('filters/', views.FilterView.as_view(), name='filters'),
    path('tejidos/', views.MuestraFilterAPIView.as_view(), name='tejidos'),
    path('tejidos/<int:id>/', views.MuestraDetailAPIView.as_view(), name='tejido-detail'),
    path('muestras/filtrado/', views.MuestraViewSet.as_view({'get': 'Filtrado'}), name='muestras_filtrado'),
    path('login/', LoginView.as_view(), name='login'),
    path('profesores/create/', views.ProfesorCreateView.as_view(), name='profesor-create'),
    path('uplimage/', views.UplimageView.as_view(), name='uplimage'),
    path('', include(router.urls)),
]
