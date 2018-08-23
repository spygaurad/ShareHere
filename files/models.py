from django.db import models
import os
from django.urls import reverse
from django.conf import settings
# Create your models here.


class Directory(models.Model):
    dir_name = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=True, max_length=50)

    def __str__(self):
        return self.dir_name


def get_file_path(instance, filename):
    directory = 'media/' + instance.dir_name
    return 'media/'


# class Files(models.Model):
#     dir_name = models.ForeignKey(Directory, on_delete=models.CASCADE)
#     #file = models.FileField(upload_to='')
#     file = models.FileField()
#
#     def __str__(self):
#         return self.dir_name + "    -" + self.file_name

