from rest_framework import serializers
from .models import Flores, Categoria



class CategoriaSerializer(serializers.ModelSerializer):
   

    class Meta:
        model = Categoria 
        fields = '__all__'



class FloresSerializer(serializers.ModelSerializer):

   

    class Meta:
        model =  Flores
        fields = ['name', 'precio', 'descripcion', 'estado','stock','imagen','Categoria']