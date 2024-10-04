from django.shortcuts import render,get_object_or_404,redirect
#---->Importamos el Sector de Formularios
from .forms import *
from .models import *
#--->Importamos la Libreria de Logout
from django.contrib.auth import logout
#--->Importamos la Libreria de Permisos
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
# Create your views here.
def Home(request):
    buscar=Productos.objects.all().order_by('-id_producto')[:3]
    data={
        'forms':buscar
    }
    return render (request,'index.html',data)

def ver_Productos(request):
    #--->TREAMOS TODOS LOS ELEMENTOS DEL TABLA
    buscar=Productos.objects.all()
    data={
        'forms':buscar
    }
    return render(request,'Pages/visualizar.html',data)

@login_required

@permission_required('App.add_personajes')
def Agregar(request):
    data={
        'forms':NuevoProducto()
    }
    if request.method=='POST':
        query=NuevoProducto(data=request.POST,files=request.FILES)
        if  query.is_valid():
            query.save()
            data['mensaje']="Datos Registrados"
        else:
            data['forms']=NuevoProducto
    return render (request,'Pages/agregar.html',data)


@permission_required('App.change_personajes')
def Modificar_Productos(request,id_producto):
    sql=get_object_or_404(Productos,id_producto=id_producto)
    data={
        'forms':NuevoProducto(instance=sql)
    }
    if request.method=='POST':
        query=NuevoProducto(data=request.POST,instance=sql,files=request.FILES)
        if  query.is_valid():
            query.save()
            data['mensaje']="Datos Modificados Correctamente "
        else:
            data['forms']=NuevoProducto
    return render (request,'Pages/modificar.html',data)


@permission_required('App.delete_personajes')
def Eliminar_Productos(request,id_producto):
    buscar=get_object_or_404(Productos,id_producto=id_producto)
    buscar.delete()
    return redirect(to="visualizar")


def salir(request):
    logout(request)
    return redirect(to='inicio')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User, Carrito, Carrito_detalle, Productos

@login_required
def Comprar(request, id_producto):
    try:
        usuario = User.objects.get_by_natural_key(request.user.username)

        # Obtener o crear el carrito
        carrito, created = Carrito.objects.get_or_create(carrito_id=request.user.id, user=usuario)

        # Obtener el producto
        producto = get_object_or_404(Productos, id_producto=id_producto)

        # Crear el detalle del carrito
        carritoDet = Carrito_detalle.objects.create(carrito_det=carrito, producto=producto, cantidad=1)
        carritoDet.save()

        messages.success(request, "Operación realizada con éxito.")
        return redirect(to="inicio")
        
    except Exception as e:
        messages.error(request, f"Error al procesar la compra: {str(e)}")
        print(e)
        return redirect(to="inicio")

def VerCarrito (request):
    #sql = Carrito_detalle.objects.select_related('carrito_det','producto').all().filter(carrito_det__user=request.user.username)
    try:
        sql = Carrito_detalle.objects.filter(carrito_det__user=request.user.id)

        data = {
            'forms':sql
        }
        return render(request,"Pages/carrito.html",data)
    except Carrito_detalle.DoesNotExist:
        return render (request,"index.html",{"err":"Carrito no encontrado"})
def EliminarCarrito (request,pk_carritodet):
    try:
        buscar=get_object_or_404(Carrito_detalle,pk_carritodet=pk_carritodet)
        buscar.delete()
        return redirect(to="carrito")
    except Carrito_detalle.DoesNotExist:
        return render (request,"index.html",{"err":"Este producto no puede ser eliminado: " + pk_carritodet})