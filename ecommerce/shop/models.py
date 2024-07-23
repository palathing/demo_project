from django.db import models

# Create your models here.

class Category(models.Model):
    cname=models.CharField(max_length=20)
    cdesc=models.TextField()
    cimage=models.ImageField(upload_to='media/image',blank=True,null=True)

    def __str__(self):
        return self.cname


class Product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to='media/products',blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True) #one tile
    updated=models.DateTimeField(auto_now=True) #change every item we update on record
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.name