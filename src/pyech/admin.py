from django.contrib import admin
from .models import UploadFile,CustomChartFile
# Register your models here.
admin.site.register(UploadFile)
admin.site.register(CustomChartFile)