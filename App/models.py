from django.db import models
from ckeditor import fields
# Create your models here.
class Productos(models.Model):
    id_producto = models.IntegerField(primary_key=True, null=False)
    nom_producto = models.TextField(max_length=50, null=False)
    desc_producto = fields.RichTextField(null=True)
    precio_producto = models.IntegerField(null=False)
    precioreb_producto = models.IntegerField(null=True)
    stock_producto = models.IntegerField(null=False)
    imagen_producto = models.ImageField(null=False,upload_to="productos", default="")
    def __int__ (self):
        return self.id_producto

