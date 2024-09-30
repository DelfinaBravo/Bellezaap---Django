from django.urls import path
#-->Importamos las Vistas para las URL
from .views import *

urlpatterns = [
    #-->URL, FUNCION, NOMBRE PARA HTML
    path('',Home,name='inicio'),
    path('agregar/',Agregar,name='agregar'),
    path('visualizar/',ver_Productos,name='visualizar'),
    path('modificar/<Codigo>/',Modificar_Productos,name='modificar'),
    path('eliminar/<Codigo>/',Eliminar_Productos,name='eliminar'),
    path('logouts/',salir,name='logouts'),
]
