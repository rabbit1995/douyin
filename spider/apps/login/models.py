from django.db import models

# Create your models here.
#数据表的模型
class User(models.Model):
    username=models.CharField(max_length=64,unique=True)
    password=models.CharField(max_length=256)
    email=models.EmailField(unique=True)
    pnumber=models.CharField(max_length=11)
    sessionid=models.CharField(max_length=40,default='null')
    c_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
    class meta:
        ordering=['-c_time']
        verbose_name='用户'
        verbose_name_plural='用户'
