from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('comic/<int:pk>/', views.detalle, name='detalle'),
]