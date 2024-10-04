from django.shortcuts import render,get_object_or_404,redirect
#---->Importamos el Sector de Formularios
from .forms import *
from .models import *
#--->Importamos la Libreria de Logout
from django.contrib.auth import logout
#--->Importamos la Libreria de Permisos
from django.contrib.auth.decorators import login_required, permission_required

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

@login_required
def Comprar (request,id_producto):
    try:
        usuario = User.objects.get_by_natural_key(request.user.username)

        carrito = Carrito.objects.all().get_or_create(carrito_id=request.user.id,user=usuario)
        carritoDet = Carrito_detalle.objects.create(carrito_det=Carrito.objects.last(),producto=get_object_or_404(Productos,id_producto=id_producto),cantidad=1)
        carritoDet.save()
        return render (request,"index.html",{"data":"Producto añadido"})    
    except Carrito.DoesNotExist:
            try:
                NCarr = Carrito(user=usuario)
                NCarr.save()
            except NCarr.DoesNotExist:
                return render (request,"index.html",{"data":"Carrito no encontrado"})
def VerCarrito (request):
    #sql = Carrito_detalle.objects.select_related('carrito_det','producto').all().filter(carrito_det__user=request.user.username)
    try:
        sql = Carrito_detalle.objects.filter(carrito_det__user=request.user.id)

        data = {
            'forms':sql
        }
        return render(request,"Pages/carrito.html",data)
    except Carrito_detalle.DoesNotExist:
        return render (request,"index.html",{"data":"Carrito no encontrado"})