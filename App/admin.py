from django.contrib import admin
#--->Traemos la Tablas desde MODELS
from .models import *

# Register your models here.
admin.site.register(Productos)
admin.site.register(Carrito_detalle)
admin.site.register(Carrito)