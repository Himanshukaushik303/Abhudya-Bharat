# Generated by Django 3.2.5 on 2021-09-04 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20210904_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrepreneurs',
            name='ent_pincode',
            field=models.DecimalField(decimal_places=0, max_digits=6, unique=True),
        ),
    ]
