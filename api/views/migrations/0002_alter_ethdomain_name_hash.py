# Generated by Django 3.2 on 2023-03-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethdomain',
            name='name_hash',
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
    ]