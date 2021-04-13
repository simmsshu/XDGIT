from django.db import models
class User(models.Model):
    username=models.CharField(max_length=100,verbose_name='用户注册')
    password =models.CharField(max_length=100,verbose_name='用户密码')
    create_time=models.DateTimeField(auto_now_add=True)#第一次创建的时间
    def __str__(self):
        return '用户名：%s'%(self.username)