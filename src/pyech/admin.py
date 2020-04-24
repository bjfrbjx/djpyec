from django.contrib import admin
from .models import UploadFile,CustomChartFile,CacheChartRender
# Register your models here.
admin.site.register(UploadFile)
admin.site.register(CacheChartRender)
admin.site.register(CustomChartFile)