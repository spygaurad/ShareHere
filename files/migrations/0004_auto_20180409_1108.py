# Generated by Django 2.0.4 on 2018-04-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20180408_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.FileField(default='files/media/group_Deerwalk.jpg', upload_to='media/'),
        ),
    ]