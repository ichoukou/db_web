from django.db import models

# Create your models here.
class BDT(models.Model):        #对大数据需求最剧烈的行业排名
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    count=models.IntegerField()

    def __str__(self):
        return self.name

class ITC(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    count=models.IntegerField()

    def __str__(self):
        return self.name

class ITS(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    salary=models.FloatField()

    def __str__(self):
        return self.name

class BDC(models.Model):        #对大数据需求最多的10个城市
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    salary=models.FloatField(null=True)
    count=models.IntegerField()

    def __str__(self):
        return self.name

class CSR(models.Model):        #工资最高的10个城市
    id=models.IntegerField(primary_key=True)
    city=models.CharField(max_length=100)
    salary=models.FloatField()

    def __str__(self):
        return self.city

class BPS(models.Model):        #大数据职位需求量排名以及工资
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=100)
    salary=models.FloatField()
    count=models.IntegerField()

    def __str__(self):
        return self.name