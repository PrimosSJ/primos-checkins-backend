# Generated by Django 4.0.3 on 2022-04-07 01:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Primo',
            fields=[
                ('rol', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('nick', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('rol', models.IntegerField(primary_key=True, serialize=False)),
                ('correo', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id_turno', models.AutoField(primary_key=True, serialize=False)),
                ('llegada', models.DateTimeField()),
                ('salida', models.DateTimeField()),
                ('rol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracks.primo')),
            ],
        ),
    ]