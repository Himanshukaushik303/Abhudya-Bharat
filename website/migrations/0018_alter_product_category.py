# Generated by Django 3.2.5 on 2021-09-26 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0017_alter_entrepreneurs_ent_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='website.Categories'),
        ),
    ]
