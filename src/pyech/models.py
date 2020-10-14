from django.db import models
from login.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.core.files.storage import FileSystemStorage
from djpyec.settings import MEDIA_ROOT
import os
from django.template.defaultfilters import default
# # Create your models here.


class file_storage(FileSystemStorage):
    def get_available_name(self, name,max_length=None):
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name

def user_directory_path(instance, filename):
    return "./upload/"+instance.author.name+"/"+filename

def user_chartfile_path(instance, filename):
    print(filename)
    return "./download/"+instance.author.name+"/"+filename

class UploadFile(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    uploadfile=models.FileField(upload_to=user_directory_path, blank=True,storage=file_storage(),unique=True) #指定的upload目录相对于根目录下media目录
     
    def __unicode__(self):
        return self.author.name

    def __str__(self):
        return self.uploadfile.name
    class Meta:
        verbose_name = "上传文件"
        verbose_name_plural= "上传文件csv"
    
class CustomChartFile(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    ChartPath=models.FileField(upload_to=user_chartfile_path, blank=True,storage=file_storage()) #指定的upload目录相对于根目录下media目录
     
    def __unicode__(self):
        return self.author.name

    def __str__(self):
        return self.ChartPath.name
    class Meta:
        verbose_name = "下载文件"
        verbose_name_plural= "下载文件html"

class CacheChartRender(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    chartid=models.CharField(max_length=64,unique=True)
    charttitle=models.CharField(max_length=64,default="默认标题")
    chartrender_text=models.BinaryField()
    class Meta:
        verbose_name = "缓存图表文件"
        verbose_name_plural= "缓存图表文件-pickle码"
@receiver(pre_delete, sender=UploadFile)
def upload_delete(sender, instance, **kwargs):
    instance.uploadfile.delete(False)

@receiver(pre_delete, sender=CustomChartFile)
def dowload_delete(sender, instance, **kwargs):
    instance.ChartPath.delete(False)