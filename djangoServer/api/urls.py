from django.urls import path, include
from rest_framework import routers
from api import views
from api.views import lista_imagenes
router = routers.DefaultRouter()
router.register(r'muestra', views.CapturaViewSet)

urlpatterns = [
    path('imagenes/', views.lista_imagenes, name='lista_imagenes'),
    path('', include(router.urls)),
]
