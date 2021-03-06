# Generated by Django 2.0.4 on 2018-04-09 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_auto_20180409_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=30)),
                ('file_type', models.CharField(max_length=10)),
                ('file', models.FileField(default='files/media/group_Deerwalk.jpg', upload_to='media/')),
                ('dir_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.Directory')),
            ],
        ),
        migrations.RemoveField(
            model_name='files',
            name='dir_name',
        ),
        migrations.DeleteModel(
            name='Files',
        ),
    ]
