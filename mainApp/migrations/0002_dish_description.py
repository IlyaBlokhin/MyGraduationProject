# Generated by Django 3.2.5 on 2021-08-14 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='description',
            field=models.CharField(default='Хрустящие вафли с малиной и сливочным мороженным', max_length=250),
            preserve_default=False,
        ),
    ]
