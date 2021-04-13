from django.db import models

class PubName(models.Model):
    pubname=models.CharField('名称',max_length=255,unique=True)

class Author(models.Model): #创建作者表
    name    =   models.CharField(max_length=30,verbose_name='姓名',default="")
    email   =   models.EmailField(verbose_name='邮箱',default="")
    books = models.ManyToManyField(to="Book")
    def __str__(self):
        return '作者：%s'%(self.name)

class Book(models.Model):
    title   =   models.CharField(max_length=30,unique=True,verbose_name="书名",default="")
    public  =   models.CharField(max_length=50,verbose_name="出版社",default="")
    price   =   models.DecimalField(max_digits=9,decimal_places=2, verbose_name="價格",default="")
    retail_price    =   models.DecimalField(max_digits=9,decimal_places=2,verbose_name="零售价",default=30)
    pub     =   models.ForeignKey(to=PubName,on_delete=models.CASCADE,default="")
    authors = models.ManyToManyField(Author)
    def __str__(self):
        return f"title:{self.title} pub:{self.public} price:{self.price}"

class UserInfo(models.Model): #创建用户信息表
    username    =   models.CharField(max_length=24,verbose_name='用户注册',default="")
    password    =   models.CharField(max_length=24,verbose_name='密码',default="")

class ExtendUserinfo(models.Model):
    user=models.OneToOneField(to=UserInfo,on_delete=models.CASCADE)
    signature=models.CharField(max_length=255,verbose_name='用户签名',help_text='自建签名')
    nickname=models.CharField(max_length=255,verbose_name='昵称',help_text='自建昵称')