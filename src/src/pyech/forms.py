# #  -*- coding:utf-8 -*-
# from django.forms import ModelForm
# from .models import UploadFile
# class UploadFileForm(ModelForm):
#     class Meta:
#         model = UploadFile      #对应的Model中的类
#         fields = ("uploadfile","author")      #字段，如果是__all__,就是表示列出所有的字段
#         exclude = None          #排除的字段
#         labels = None           #提示信息
#         help_texts = None       #帮助提示信息
#         widgets = None          #自定义插件
#         error_messages = {
#             'uploadfile':{'required':"文件不能为空",},
#         }
#     def __init__(self, *args, **kwargs):
#         super(UploadFileForm, self).__init__(*args, **kwargs)
#         self.fields['author'].required = False