#  -*- coding:utf-8 -*-
from django.db import models


class User(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )

    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='��')
    regist_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['regist_time']
        verbose_name = "用户"
        verbose_name_plural = '用户'

class running_list(models.Model):
    status_list=(
        ("执行成功","执行成功"),
        ("执行失败","执行失败"),
        ("执行中","执行中"))
    name = models.CharField(max_length=128,unique=True)
    user = models.CharField(max_length=128)
    fun = models.CharField(max_length=128)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    sum_time = models.TimeField(blank=True, null=True)
    status =models.CharField(max_length=32,choices=status_list,default='执行中')
    