# Generated by Django 3.2.5 on 2021-09-04 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20210904_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bussiness_partner',
            name='bp_number',
            field=models.DecimalField(decimal_places=0, max_digits=10, unique=True),
        ),
        migrations.AlterField(
            model_name='bussiness_partner',
            name='founder_number',
            field=models.DecimalField(decimal_places=0, max_digits=10, unique=True),
        ),
        migrations.AlterField(
            model_name='bussiness_partner',
            name='incorporation_year',
            field=models.DecimalField(decimal_places=0, max_digits=4, unique=True),
        ),
        migrations.AlterField(
            model_name='entrepreneurs',
            name='ent_aadhar',
            field=models.DecimalField(decimal_places=0, max_digits=12, unique=True),
        ),
        migrations.AlterField(
            model_name='entrepreneurs',
            name='ent_number',
            field=models.DecimalField(decimal_places=0, max_digits=10, unique=True),
        ),
        migrations.AlterField(
            model_name='entrepreneurs',
            name='ent_pincode',
            field=models.DecimalField(decimal_places=0, max_digits=5, unique=True),
        ),
    ]