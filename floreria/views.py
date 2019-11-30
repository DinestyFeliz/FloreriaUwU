from django.shortcuts import render
from .models import Categoria,Flores #importar los modelos desde el archivo models.py
 #definir los metodos con un login requerido
from django.contrib.auth.decorators import login_required
#debemos incluir el modelo de users del sistema
from django.contrib.auth.models import User
#incluimos el sistema de autentificacion de Django, 
#le di un alias a 'login'
from django.contrib.auth import authenticate,logout, login as auth_login
# Create your views here.

def agregar_carrito(request,id):
    #recuperar la lista del carrito desde la sesion
    lista=request.session.get("carrito","")
    #agregar el titulo a listado
    lista=lista+str(id)+str(";")
    #volver a ingresarlo a la sesion
    request.session["carrito"]=lista
    return render(request,"core/carrito.html",{'listaCarrito':lista})

def eliminar_flores(request,id):
    flor=Flores.objects.get(name=id)#buscar Flor
    msg=''
    try:
        flor.delete()# elimino
        msg='Elimino Flores'
    except:
        msg='No Elimino'
    lFlor=Flores.objects.all()# selecciono todo
    return render(request,"core/galeria.html",{'lista':lFlor,'msg':msg})
    

def login(request):
    return render(request,"core/login.html")

def cerrar_sesion(request):
    logout(request)
    return render(request,"core/login.html",{'msg':'Cerro Sesión'})
    
def login_acceso(request):
    if request.POST:
        usuario=request.POST.get("txtUser")
        password=request.POST.get("txtPass")
        #creamos un modelo de usuario para autentificar
        us = authenticate(request,username=usuario,password=password)
        if us is not None and us.is_active:
            auth_login(request,us)
            return render(request,"core/index.html")
    return render(request,"core/login.html",{'msg':'Datos Incorrectos'})

@login_required(login_url='/login/')
def index(request):
    return render(request,'core/index.html')

@login_required(login_url='/login/')
def gale(request):
    flor=Flores.objects.all()#select * from Peliculas
    return render(request,'core/galeria.html',{'lista':flor})

@login_required(login_url='/login/')
def formulario(request):
    categorias=Categoria.objects.all() # select * form Categoria
    if request.POST:
        # recuperar el valor del boton accion
        accion=request.POST.get("accion")
        if accion=='grabar':            
            titulo=request.POST.get("txtNombre")
            precio=request.POST.get("txtPrecio")
            descrip=request.POST.get("txtDescripcion")
            catego=request.POST.get("cboCategoria")
            estadito=request.POST.get("chboEstado")
            if estadito=="on":
                estadeste='True'
            else:
                estadeste='False'
            cant=request.POST.get("txtStock")
            imagen=request.FILES.get("txtImagen")
            obj_categoria=Categoria.objects.get(name=catego)
            #instanciar un objeto (modelo) Pelicula
            flor=Flores(
                name=titulo,
                precio=precio,
                descripcion=descrip,
                estado=estadeste,
                stock=cant,
                imagen=imagen,
                Categoria=obj_categoria
            )
            flor.save() #graba los datos del modelo
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'Grabo'})
        if accion=='eliminar':
            nombre=request.POST.get("txtNombre")#recupera el titulo
            flor=Flores.objects.get(name=nombre)# lo busca entre las Flores
            flor.delete()#elimina
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'Elimino'})
    return render(request,'core/formulario.html',{'listacategoria':categorias})

@login_required(login_url='/login/')
def quienes_somos(request):
    return render(request,'core/quienes_somos.html')

def password_reset_confirm(request):
    return render(request,'core/password_reset_confirm.html')

def password_reset_done(request):
    return render(request,'core/password_reset_done.html')

def password_reset_email(request):
    return render(request,'core/password_reset_email.html')

def password_reset_form(request):
    return render(request,'core/password_reset_form.html')

def password_reset_complete(request):
    return render(request,'core/password_reset_complete.html')
