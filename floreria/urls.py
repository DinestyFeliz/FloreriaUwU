from django.contrib import admin
from django.urls import path, re_path, include 
from .views import *
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy

urlpatterns = [
    path('', index,name='IND'),
    path('galeria/',gale,name='GAL'),
    path('proximamente/',prox,name='PROX'),
    path('formulario/',formulario,name='FORMU'),
    path('quienes_somos/',quienes_somos,name='QUIEN'),
    path('login/',login,name='LOGIN'),
    path('login_acceso/',login_acceso,name='LOGINACCESO'),
    path('cerrar_sesion/',cerrar_sesion,name='CERRARSESION'),
    path('eliminar_flores/<id>/',eliminar_flores,name='ELIMINA'),
    path('agregar_carro/<id>/',carro_compras,name='AGREGAR_CARRO'),
    path('carro/',carros,name='CARRITO'),
    path('carro_mas/<id>/',carro_compras_mas,name='CARRO_MAS'),
    path('carro_menos/<id>/',carro_compras_menos,name='CARRO_MENOS'),
    path('grabar_carro/',grabar_carro,name='GRABAR_CARRO'),
    path('vaciar_carrito/',vacio_carrito,name='VACIARCARRITO'),
    path('oauth/',include('social_django.urls',namespace='social')),
    path('', include('pwa.urls')), #url service worker
    #guardar token
    path('guardar_token/', guardar_token, name='guardar_token'),
    #registro de usuario
    path('registro',registro_usuario, name='registro_usuario'),
    #recuperar contraseña
    path('reset/password_reset', PasswordResetView.as_view(template_name='registration/password_reset_form.html', email_template_name="registration/password_reset_email.html"), name = 'password_reset'),
    path('reset/password_reset_done', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name = 'password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-za-z_\-]+)/(?P<token>.+)/$', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('reset/done',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html') , name = 'password_reset_complete'),
]

    
    