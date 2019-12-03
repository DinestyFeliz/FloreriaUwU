from django.shortcuts import render
from .models import Categoria,Flores #importar los modelos desde el archivo models.py
 #definir los metodos con un login requerido
from django.contrib.auth.decorators import login_required, permission_required
#debemos incluir el modelo de users del sistema
from django.contrib.auth.models import User
#incluimos el sistema de autentificacion de Django, 
#le di un alias a 'login'
from django.contrib.auth import authenticate,logout, login as auth_login
# Create your views here.

#imports para guardar los tokens
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpRequest, HttpResponseBadRequest

from django.core import serializers
import json

from fcm_django.models import FCMDevice

@csrf_exempt
@require_http_methods(['POST'])
def guardar_token(request):
    body = request.body.decode('utf-8')
    bodyDict = json.loads(body)

    token = bodyDict('token')

    existe = FCMDevice.objects.filter(registration_id = token, active=True)

    if len(existe) > 0:
        return HttpResponseBadRequest(json.dumps({'mensaje':'el token ya existe'}))

    dispositivo = FCMDevice()
    dispositivo.registration_id = token
    dispositivo = True

    #solo si el usuario esta autenticado procederemos a enlazarlo
    if request.user.is_authenticated:
        dispositivo.user = request.user
    
    try:
        dispositivo.save()
        return HttpRequest(json.dumps({'mensaje':'token guardado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje':'no se ha podido guardar'}))

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
    return render(request,"registration/login.html")

def cerrar_sesion(request):
    logout(request)
    return render(request,"registration/login.html",{'msg':'Cerro Sesión'})
    
def login_acceso(request):
    if request.POST:
        usuario=request.POST.get("txtUser")
        password=request.POST.get("txtPass")
        #creamos un modelo de usuario para autentificar
        us = authenticate(request,username=usuario,password=password)
        if us is not None and us.is_active:
            auth_login(request,us)
            return render(request,"core/index.html")
    return render(request,"registration/login.html",{'msg':'Datos Incorrectos'})

def index(request):
    return render(request,'core/index.html')

@login_required(login_url='/login/')
def gale(request):
    flor=Flores.objects.all()#select * from Peliculas
    return render(request,'core/galeria.html',{'lista':flor})

@permission_required('core.puede_agregar_flores')
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
            #instanciar un objeto (modelo) Flores
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

            #recuperamos a todos los dispositivos
            dispositivos = FCMDevice.objects.filter(active=True)
            dispositivos.send_message(
                title="Nuevo Articulo Agregado!!!",
                body="Se ha agregado " + formulario.cleaned_data['nombre'],
                icon="/static/img/icon.png"
            )

            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'Grabo'})
        if accion=='eliminar':
            nombre=request.POST.get("txtNombre")#recupera el titulo
            flor=Flores.objects.get(name=nombre)# lo busca entre las Flores
            flor.delete()#elimina
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'Elimino'})
    return render(request,'core/formulario.html',{'listacategoria':categorias})

#def registrar_usuario(request):
#
#    if request.POST:
#        # recuperar el valor del boton accion
#        accion=request.POST.get("accion")
#        if accion=='Registrar':            
#            nombre=request.POST.get("txtNombre")
#            email=request.POST.get("txtCorreo")
#            password1=request.POST.get("txtContraseña")
#            password2=request.POST.get("txtContraseña_confirm")
#            if password1==password2:
#                contraseña=password1
#            else:
#                return render(request,'registration/registrat.html',{'listacategoria':categorias,'msg':'Contraseña no valida'})
#                
#            #instanciar un objeto user
#            User=usuario(
#                username=nombre,
#                email=email,
#                password=contraseña,
#            )
#            User.save() #graba los datos del modelo
#            return render(request,registration/registrat.html,{'listacategoria':categorias,'msg':'Usuario Creado'})
#    return render(request, 'registration/registrar.html')

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
