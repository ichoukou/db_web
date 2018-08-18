from django.db import models

# Create your models here.


class lgzp(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    mon_wa=models.CharField(max_length=20)
    education=models.CharField(max_length=20)
    work_exp=models.CharField(max_length=20)
    work_lable=models.CharField(max_length=100)
    work_desp=models.CharField(max_length=10000)
    work_area=models.CharField(max_length=20)

    def __str__(self):
        return self.name


class qtzp(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    mon_wa = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    work_exp = models.CharField(max_length=20)
    work_lable = models.CharField(max_length=100)
    work_desp = models.CharField(max_length=10000)
    work_area = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class zlzp(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    mon_wa = models.CharField(max_length=20)
    education = models.CharField(max_length=20)
    work_exp = models.CharField(max_length=20)
    work_lable = models.CharField(max_length=100)
    work_desp = models.CharField(max_length=10000)
    work_area = models.CharField(max_length=20)
    leibie=models.CharField(max_length=50)
    def __str__(self):
        return self.name


