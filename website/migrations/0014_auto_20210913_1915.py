# Generated by Django 3.2.5 on 2021-09-13 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_alter_entrepreneurs_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='website.categories'),
        ),
    ]
