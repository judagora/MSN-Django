# Generated by Django 5.1.6 on 2025-03-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inicio', '0002_remove_usuario_contraseña_usuario_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='peritaje',
            name='costo',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='peritaje',
            name='notas_adicionales',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='peritaje',
            name='descripcion',
            field=models.CharField(max_length=255),
        ),
    ]
