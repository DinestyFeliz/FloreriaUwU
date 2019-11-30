from django.db import models

# Create your models here.

class Categoria(models.Model):
    name=models.CharField(max_length=45, primary_key=True)
    categoria=models.IntegerField()

    def __str__(self):
        return self.name

class Flores(models.Model):
    name=models.CharField(max_length=45, primary_key=True)
    precio=models.IntegerField()
    descripcion=models.TextField()
    estado=models.BooleanField()
    stock=models.IntegerField()
    imagen=models.ImageField(upload_to='flores',null=True)

    Categoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)

    def __str__(self):
        return self.name