# Generated by Django 3.2.5 on 2021-09-04 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product_Video',
        ),
        migrations.AddField(
            model_name='product_image',
            name='product_video',
            field=models.FileField(null=True, upload_to='product_video'),
        ),
    ]