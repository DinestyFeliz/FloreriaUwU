from django.shortcuts import render
from .models import Categoria,Flores,Ticket #importar los modelos desde el archivo models.py
 #definir los metodos con un login requerido
from django.contrib.auth.decorators import login_required, permission_required
#debemos incluir el modelo de users del sistema
from django.contrib.auth.models import User
#incluimos el sistema de autentificacion de Django, 
#le di un alias a 'login'
from django.contrib.auth import authenticate,logout, login as auth_login
# Create your views here.
import datetime;
from .elemento import elemento

#imports para guardar los tokens
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseBadRequest

from django.core import serializers
import json

from fcm_django.models import FCMDevice
#registro de usuario
from .forms import CustomUserForm
from django.contrib.auth import login, authenticate

from rest_framework import viewsets
from.serializers import FloresSerializer, CategoriaSerializer

class FloresViewSet(viewsets.ModelViewSet):
    queryset = Flores.objects.all()
    serializer_class = FloresSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

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
    dispositivo.active = True

    #solo si el usuario esta autenticado procederemos a enlazarlo
    if request.user.is_authenticated:
        dispositivo.user = request.user
    
    try:
        dispositivo.save()
        return HttpResponse(json.dumps({'mensaje':'token guardado'}))
    except:
        return HttpResponseBadRequest(json.dumps({'mensaje':'no se ha podido guardar'}))



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


@csrf_exempt
def login(request):
    if request.POST:
        usuario=request.POST.get("txtUsuario")
        password=request.POST.get("txtPass")
        us=authenticate(request,username=usuario,password=password)
        msg=''
        request.session["carrito"] = []        
        request.session["carritox"] = []        
        print('realizado')
        if us is not None and us.is_active:
            auth_login (request,us)#autentificacion de login            
            return render(request,'core/index.html')
        else:
            return render(request,'registration/login.html')
    return render(request,"registration/login.html")



def cerrar_sesion(request):
    logout(request)
    return render(request,"registration/login.html",{'msg':'Cerro Sesión'})
    
@csrf_exempt   
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
    flor=Flores.objects.all()#select * from flores
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
                body="Se ha agregado " + request.POST.get("txtNombre"),
                icon="/static/img/logo-floreria.png"
            )

            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'Grabo'})
        if accion=='eliminar':
            nombre=request.POST.get("txtNombre")#recupera el titulo
            flor=Flores.objects.get(name=nombre)# lo busca entre las Flores
            flor.delete()#elimina
            return render(request,'core/formulario.html',{'listacategoria':categorias,'msg':'Elimino'})
    return render(request,'core/formulario.html',{'listacategoria':categorias})

#registro de usuario
@csrf_exempt
def registro_usuario(request):
    data = {
        'form':CustomUserForm()
    }
    if request.method == 'POST':
        formulario = CustomUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            #autenticar al usuario y redirigirlo al inicio
            usuario=request.POST.get("username")
            password=request.POST.get("password1")
            us = authenticate(request,username=usuario,password=password)
            if us is not None and us.is_active:
                auth_login(request,us)
                return render(request,"core/index.html")
        return render(request, 'registration/registrar.html', data, {'msg':'Error con los datos'})
    return render(request, 'registration/registrar.html', data)

#carrito
@login_required(login_url='/login/')
def vacio_carrito(request):
    request.session["carritox"]=""
    lista=request.session.get("carrito","")
    return render(request, "core/carrito.html", {'lista':lista})

@login_required(login_url='/login/')
def carros(request):
    x=request.session["carritox"]
    suma=0
    for item in x:
        suma=suma+int(item["total"])           
    return render(request,'core/carrito.html',{'x':x,'total':suma})  

@login_required(login_url='/login/')
def grabar_carro(request):
    x=request.session["carritox"]    
    usuario=request.user.username
    suma=0
    try:
        for item in x:        
            titulo=item["nombre"]
            precio=int(item["precio"])
            cantidad=int(item["cantidad"])
            total=int(item["total"])        
            ticket=Ticket(
                usuario=usuario,
                titulo=titulo,
                precio=precio,
                cantidad=cantidad,
                total=total,
                fecha=datetime.date.today()
            )
            ticket.save()
            suma=suma+int(total)  
            print("reg grabado")                 
        mensaje="Grabado"
        request.session["carritox"] = []
    except:
        mensaje="error al grabar"            
    return render(request,'core/carrito.html',{'x':x,'total':suma,'mensaje':mensaje})

@login_required(login_url='/login/')
def carro_compras(request,id):
    p=Flores.objects.get(name=id)
    x=request.session["carritox"]
    el=elemento(1,p.name,p.precio,1)
    sw=0
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==p.name:
            sw=1
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["precio"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    if sw==0:
        clon.append(el.toString())
    x=clon    
    request.session["carritox"]=x
    flor=Flores.objects.all()    
    return render(request,'core/galeria.html',{'lista':flor,'total':suma})

@login_required(login_url='/login/')
def carro_compras_mas(request,id):
    p=Flores.objects.get(name=id)
    x=request.session["carritox"]
    suma=0
    clon=[]
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==p.name:
            cantidad=int(cantidad)+1
        ne=elemento(1,item["nombre"],item["precio"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]        
    return render(request,'core/carrito.html',{'x':x,'total':suma})

@login_required(login_url='/login/')
def carro_compras_menos(request,id):
    p=Flores.objects.get(name=id)
    x=request.session["carritox"]
    clon=[]
    suma=0
    for item in x:        
        cantidad=item["cantidad"]
        if item["nombre"]==p.name:
            cantidad=int(cantidad)-1
        ne=elemento(1,item["nombre"],item["precio"],cantidad)
        suma=suma+int(ne.total())
        clon.append(ne.toString())
    x=clon    
    request.session["carritox"]=x
    x=request.session["carritox"]    
    return render(request,'core/carrito.html',{'x':x,'total':suma})

def quienes_somos(request):
    return render(request,'core/quienes_somos.html')

def prox(request):
    return render(request,'core/proximamente.html')

def password_reset_confirm(request):
    return render(request,'registration/password_reset_confirm.html')

def password_reset_done(request):
    return render(request,'registration/password_reset_done.html')

def password_reset_email(request):
    return render(request,'registration/password_reset_email.html')

def password_reset_form(request):
    return render(request,'registration/password_reset_form.html')

def password_reset_complete(request):
    return render(request,'registration/password_reset_complete.html')

def isset(variable):
	return variable in locals() or variable in globals()
