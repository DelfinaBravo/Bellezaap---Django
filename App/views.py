from datetime import date
from operator import index
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required

# Importaciones para la autenticación y registro
from django.contrib.auth import login, authenticate
from .forms import * 
from .models import *
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import render_to_string
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.conf import settings
from django.http import JsonResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.conf import settings
from django.http import JsonResponse


@login_required
def generar_boleta(request):
    context = {
        'current_date': date.today(),
    }
    try:
        # Obtener el carrito del usuario autenticado
        carrito = Carrito.objects.get(user=request.user)

        # Verificar si el carrito tiene productos
        if not carrito.carrito_detalle_set.exists():
            messages.error(request, "El carrito está vacío. Agregue productos antes de generar una boleta.")
            return redirect('carrito')

        # Crear el PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="Bellezaapp.pdf"'

        pdf = canvas.Canvas(response)
        pdf.drawString(100, 800, "Factura de Compra")
        pdf.drawString(100, 780, f"Cliente: {request.user.username}")
        pdf.drawString(100, 760, f"Fecha: {context['current_date'].strftime('%d %b %Y')}")  # Mostrar la fecha
        y = 630

        # Crear tabla
        detalles = [[
            "Producto", "Cantidad", "Precio Unitario", "Subtotal"
        ]]
        total = 0

        for detalle in carrito.carrito_detalle_set.all():
            subtotal = detalle.producto.precio_producto * detalle.cantidad
            detalles.append([
                detalle.producto.nom_producto,
                detalle.cantidad,
                f"${detalle.producto.precio_producto}",
                f"${subtotal}"
            ])
            total += subtotal

        detalles.append(["", "", "Total", f"${total}"])

        color_fondo = '#7a5b52'
        color_letras = '#5c4033'
        # Estilo de tabla
        table = Table(detalles)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color_fondo)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor(color_letras)),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ]))

        # Dibujar la tabla en el PDF
        table.wrapOn(pdf, 400, 600)
        table.drawOn(pdf, 100, y - 20)

        pdf.showPage()
        pdf.save()

        return response

    except Carrito.DoesNotExist:
        messages.error(request, "No se encontró un carrito para el usuario.")
        return redirect('inicio')

@login_required
def Factura(request):
    return render(request,'Pages/factura.html')

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
            messages.success(request, "Producto agregado corectamente!")
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
            messages.success(request, "Producto modificado con éxito.")
        else:
            data['forms']=NuevoProducto
    return render (request,'Pages/modificar.html', data)


@permission_required('App.delete_personajes')
def Eliminar_Productos(request,id_producto):
    buscar=get_object_or_404(Productos,id_producto=id_producto)
    buscar.delete()
    messages.success(request, "Producto eliminado con éxito.")
    return redirect(to="visualizar")


def salir(request):
    logout(request)
    return redirect(to='inicio')

# @login_required
# def Comprar(request, id_producto):
#     usuario = request.user  # Ya autenticado por @login_required

#     # Obtener o crear el carrito para el usuario
#     carrito, created = Carrito.objects.get_or_create(user=usuario)

#     # Obtener el producto
#     producto = get_object_or_404(Productos, id_producto=id_producto)

#     # Buscar o crear el detalle del carrito
#     carrito_detalle = Carrito_detalle.objects.filter(carrito_det=carrito,producto=producto).first()

#     if not carrito_detalle:
#         carrito_detalle = Carrito_detalle.objects.create(
#             carrito_det=carrito,
#             producto=producto,
#             cantidad=0
#         )

#     # Manejar la acción (incrementar o disminuir)
#     accion = request.GET.get('accion')
#     if accion == "incrementar":
#         carrito_detalle.cantidad += 1
#     elif accion == "disminuir" and carrito_detalle.cantidad > 0:
#         carrito_detalle.cantidad -= 1

#     # Guardar o eliminar el detalle si corresponde
#     if carrito_detalle.cantidad == 0:
#         carrito_detalle.delete()
#     else:
#         carrito_detalle.save()

#     messages.success(request, "Carrito actualizado correctamente.")
#     return redirect("carrito")

# @login_required
# def Comprar (request,id_producto):
#     try:
#         usuario = User.objects.get_by_natural_key(request.user.username)
#         carrito = Carrito.objects.all().get_or_create(carrito_id=request.user.id,user=usuario)
#         carritoDet = Carrito_detalle.objects.create(carrito_det=Carrito.objects.last(),producto=get_object_or_404(Productos,id_producto=id_producto),cantidad=1)
#         carritoDet.save()
#         messages.success(request, "Producto agregado al carrito correctamente. Gracias por elegirnos!")
#         # return render (request,"Pages/continuarCompra.html",{"data":"Producto añadido"})    
#         return redirect(to="carrito")
#     except Carrito.DoesNotExist:
#             try:
#                 NCarr = Carrito(user=usuario)
#                 NCarr.save()
#             except NCarr.DoesNotExist:
#                 messages.warning(request, "Ops!. No se pudo procesar la seleccion del producto")
#                 return render (request,"Pages/continuarCompra.html",{"data":"Carrito no encontrado"})
@login_required
def Comprar(request, id_producto):
    try:
        # Obtener el usuario autenticado
        usuario = request.user
        # Obtener o crear el carrito del usuario
        carrito, creado = Carrito.objects.get_or_create(user=usuario)
        # Obtener el producto solicitado
        producto = get_object_or_404(Productos, id_producto=id_producto)
        # Buscar o crear el detalle del carrito
        carrito_detalle, detalle_creado = Carrito_detalle.objects.get_or_create(
            carrito_det=carrito,
            producto=producto,
            defaults={"cantidad": 1},  # Cantidad inicial si es un nuevo detalle
        )
        # Manejar la acción (incrementar o disminuir)
        accion = request.GET.get('accion')  # Lee el parámetro 'accion' de la URL
        if accion == "incrementar":
            carrito_detalle.cantidad += 1
            carrito_detalle.save()
            messages.success(request, "Cantidad incrementada correctamente.")
        elif accion == "disminuir":
            if carrito_detalle.cantidad > 1:  # Evita cantidades menores a 1
                carrito_detalle.cantidad -= 1
                carrito_detalle.save()
                messages.success(request, "Cantidad disminuida correctamente.")
            else:
                carrito_detalle.delete()  # Elimina el detalle si la cantidad llega a 0
                messages.info(request, "Producto eliminado del carrito.")
        # Redirigir al usuario
        return redirect(to="carrito")
    except Exception as e:
        # Manejo de errores inesperados
        messages.error(request, f"Ocurrió un error al procesar tu solicitud: {str(e)}")
        return redirect(to="ver_Productos")

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

@login_required
def EliminarCarrito(request, pk=None):
    try:
        # Si se pasa un ID de producto (pk), eliminar solo ese producto del carrito
        if pk:
            detalle = get_object_or_404(Carrito_detalle, pk=pk, carrito_det__user=request.user)
            detalle.delete()
            messages.success(request, "Producto eliminado del carrito.")
        else:
            # Si no se pasa un ID, eliminar todos los productos del carrito
            Carrito_detalle.objects.filter(carrito_det__user=request.user).delete()
            messages.success(request, "Todos los productos han sido eliminados del carrito.")
        
        return redirect("carrito")  # Redirige al carrito después de eliminar
    except Exception as e:
        messages.error(request, f"Error al eliminar productos del carrito: {str(e)}")
        return redirect("carrito")
    
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Cambiar a SignUpForm
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(to='inicio')  # Redirigir al home después de registrarse
    else:
        form = SignUpForm()  # Crear un nuevo formulario vacío
    return render(request, 'registration/register.html', {'form': form})