# Generated by Django 4.0.3 on 2022-04-08 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_alter_primo_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turno',
            name='checkout',
            field=models.DateTimeField(null=True),
        ),
    ]