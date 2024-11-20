from django.db import models
from ckeditor import fields
from django.contrib.auth.models import User
# Create your models here.
class Productos(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.TextField(max_length=50, null=False)
    desc_producto = fields.RichTextField(null=True)
    precio_producto = models.IntegerField(null=False)
    precioreb_producto = models.IntegerField(null=True)
    stock_producto = models.IntegerField(null=False)
    imagen_producto = models.ImageField(null=False,upload_to="productos", default="")
    def __int__ (self):
        return self.id_producto

class Carrito(models.Model):
    carrito_id = models.AutoField(primary_key=True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __int__(self):
        return self.carrito_id
    
class Carrito_detalle(models.Model):
    pk_carritodet = models.AutoField(primary_key=True, null=False)
    carrito_det = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=False)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.carrito_det
    
class Comprar(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.id} - Cliente {self.cliente.username}"

class DetalleCompra(models.Model):
    id = models.AutoField(primary_key=True)
    compra = models.ForeignKey(Comprar, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto en el momento de la compra

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nom_producto} - Compra {self.compra.id}"