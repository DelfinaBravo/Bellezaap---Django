#--->Importamos 'FORMS'
from django import forms
#---> Importamos los Modelos/Tablas
from .models import *

class NuevoProducto(forms.ModelForm):
    class Meta:
        model=Productos
        fields='__all__'