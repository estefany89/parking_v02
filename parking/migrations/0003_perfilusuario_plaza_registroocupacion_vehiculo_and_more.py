# Generated by Django 5.1.6 on 2025-06-03 16:40

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking', '0002_parking'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.CharField(blank=True, max_length=15)),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('operador', 'Operador')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Plaza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10)),
                ('ocupada', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroOcupacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_entrada', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('operador_entrada', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entradas_registradas', to=settings.AUTH_USER_MODEL)),
                ('operador_salida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='salidas_registradas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_entrada'],
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('matricula', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=30)),
                ('propietario_nombre', models.CharField(max_length=100)),
                ('propietario_telefono', models.CharField(blank=True, max_length=15)),
            ],
        ),
        migrations.DeleteModel(
            name='Coche',
        ),
        migrations.AddField(
            model_name='parking',
            name='capacidad_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='parkings',
            field=models.ManyToManyField(blank=True, to='parking.parking'),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plaza',
            name='parking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plazas', to='parking.parking'),
        ),
        migrations.AddField(
            model_name='registroocupacion',
            name='plaza',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.plaza'),
        ),
        migrations.AddField(
            model_name='registroocupacion',
            name='vehiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parking.vehiculo'),
        ),
        migrations.AlterUniqueTogether(
            name='plaza',
            unique_together={('parking', 'numero')},
        ),
    ]
