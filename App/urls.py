from django.urls import path
#-->Importamos las Vistas para las URL
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    #-->URL, FUNCION, NOMBRE PARA HTML
    path( '',Home,name='inicio'),
    path('agregar/',Agregar,name='agregar'),
    path('comprar/<int:id_producto>/<int:user_id>/', Comprar, name='comprar_superusuario'), 
    path('comprar/<int:id_producto>/',Comprar,name='comprar'),
    path('carrito/',VerCarrito ,name='carrito'),
    path('carrito/eliminar/', EliminarCarrito, name='eliminar_carrito'),  # Para vaciar todo el carrito
    path('carrito/eliminar/<int:pk>/', EliminarCarrito, name='eliminar_carrito'),  # Para eliminar un producto específico
    path('visualizar/',ver_Productos,name='visualizar'),
    path('modificar/<id_producto>/',Modificar_Productos,name='modificar'),
    path('eliminar/<id_producto>/',Eliminar_Productos,name='eliminar'),
    path('logouts/',salir,name='logouts'),
    path('register/', register, name='register'),
    path('generar_boleta', generar_boleta, name='generar_boleta'),
    path('factura/',Factura, name='factura'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('ver_Productos/',ver_Productos,name='ver_Productos'),
]
