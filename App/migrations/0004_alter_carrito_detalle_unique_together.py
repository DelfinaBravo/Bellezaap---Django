# Generated by Django 5.0.6 on 2024-12-02 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_comprar_detallecompra'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='carrito_detalle',
            unique_together={('carrito_det', 'producto')},
        ),
    ]
