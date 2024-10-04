from django.urls import path
#-->Importamos las Vistas para las URL
from .views import *

urlpatterns = [
    #-->URL, FUNCION, NOMBRE PARA HTML
    path( '',Home,name='inicio'),
    path('agregar/',Agregar,name='agregar'),
    path('comprar/<id_producto>/',Comprar,name='comprar'),
    path('carrito/',VerCarrito ,name='carrito'),
    path('visualizar/',ver_Productos,name='visualizar'),
    path('modificar/<id_producto>/',Modificar_Productos,name='modificar'),
    path('eliminar/<id_producto>/',Eliminar_Productos,name='eliminar'),
    path('logouts/',salir,name='logouts'),
]
