from django.db import models

# Create your models here.

class FDT_User(models.Model):
    userName=models.CharField(max_length=200)
    pwd=models.CharField(max_length=50)
    loginTime=models.DateField("last login time")
    loginIp=models.CharField(max_length=20)
    loginAddress=models.CharField(max_length=200)

class FDT_Account(models.Model):
    
    user=models.ForeignKey(FDT_User,on_delete=models.CASCADE)
    amount=models.FloatField(default=0.0)

class FDT_User_Fund(models.Model):
    user=models.ForeignKey(FDT_User,on_delete=models.CASCADE)
    fundcode=models.CharField(max_length=10)

class FDT_UserOpHistory(models.Model):
    user=models.ForeignKey(FDT_User,on_delete=models.CASCADE)
    text=models.CharField(max_length=500)


        
        

    
        
    
        