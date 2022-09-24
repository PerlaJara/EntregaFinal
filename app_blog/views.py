import re
from typing import Dict

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from app_blog.models import *
from app_blog.forms import *

def inicio(request):
    return render(request, "app_blog/base.html")

def about(request):
    return render(request, "app_blog/about.html")

def blog(request):
    blogs = Post.objects.all()

    return render(request, "app_blog/inicio.html", {'blogs' : blogs})

#def login(request):
#    return render(request, "app_blog/login.html")


# USUARIO

@login_required
def usuario(request):
    usuarios = Usuario.objects.all()
    return render(request, "app_blog/usuarios.html", {'usuarios' : usuarios})

@login_required
def usuario_formulario(request):
    if request.method == 'POST':
        formulario= UsuarioFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data
            usuario = Usuario(nombre=data['nombre'], apellido=data['apellido'], nombre_usuario=data['nombre_usuario'], correo=data['correo'])
            usuario.save()
            return render(request, "app_blog/usuarios.html", {"exitoso": True})
    else:
        formulario= UsuarioFormulario()
    return render(request, "app_blog/crear_usuario.html", {"formulario": formulario})

@login_required
def buscar_usuario_form(request):
    return render(request, "app_blog/buscar_usuario.html")

@login_required
def buscar_usuario(request):
    if request.GET["valor"]:
        valor = request.GET["valor"]
        usuario = Usuario.objects.filter(nombre__icontains=valor) | Usuario.objects.filter(apellido__icontains=valor) | Usuario.objects.filter(nombre_usuario__icontains=valor)
        return render(request, "app_blog/usuarios.html", {'usuarios': usuario})
    else:
        return render(request, "app_blog/usuarios.html", {'usuarios': []})

@login_required
def editar_usuario(request, id):
    # Recibe param profesor id, con el que obtenemos el profesor
    usuario = Usuario.objects.get(id=id)

    if request.method == 'POST':
        formulario = UsuarioFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data

            usuario.nombre = data['nombre']
            usuario.apellido = data['apellido']
            usuario.nombre_usuario = data['nombre_usuario']
            usuario.correo = data['correo']

            usuario.save()

            return redirect(reverse('usuario'))
    else:
        inicial = {
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'nombre_usuario': usuario.nombre_usuario,
            'correo': usuario.correo,
        }
        formulario = UsuarioFormulario(initial=inicial)
    return render(request, "app_blog/crear_usuario.html", {"formulario": formulario})

def eliminar_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect(reverse('usuario'))

# POST

@login_required
def post(request):
    posts = Post.objects.all()
    return render(request, "app_blog/posts.html", {'posts' : posts})

@login_required
def post_formulario(request):
    if request.method == 'POST':
        formulario= PostFormulario(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data
            post = Post(titulo=data['titulo'], subtitulo=data['subtitulo'], imagen=data['imagen'], cuerpo=data['cuerpo'], autor=data['autor'], usuario_id=data['usuario_id'])
            post.save()
            return render(request, "app_blog/inicio.html", {"exitoso": True})
    else:
        formulario= PostFormulario()
    return render(request, "app_blog/crear_post.html", {"formulario": formulario})

@login_required
def editar_post(request, id):
    # Recibe param profesor id, con el que obtenemos el profesor
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        formulario = PostFormulario(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data

            post.titulo = data['titulo']
            post.subtitulo = data['subtitulo']
            post.imagen = data['imagen']
            post.cuerpo = data['cuerpo']

            post.save()

            return redirect(reverse('post'))
    else:
        inicial = {
            'titulo': post.titulo,
            'subtitulo': post.subtitulo,
            'imagen': post.imagen,
            'cuerpo': post.cuerpo,
        }
        formulario = PostFormulario(initial=inicial)
    return render(request, "app_blog/crear_post.html", {"formulario": formulario})

@login_required
def eliminar_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect(reverse('post'))


# COMENTARIO

@login_required
def comentario(request):
    comentarios = Comentario.objects.all()
    return render(request, "app_blog/comentarios.html", {'comentarios' : comentarios})

@login_required
def comentario_formulario(request):
    if request.method == 'POST':
        formulario= ComentarioFormulario(request.POST)

        if formulario.is_valid():
            data = formulario.cleaned_data
            comentario = Comentario(nombre_usuario=data['nombre_usuario'], comentario=data['comentario'],id_usuario=data['id_usuario'], post_id=data['post_id'])
            comentario.save()
            return render(request, "app_blog/crear_comentario.html", {"exitoso": True})
    else:
        formulario= ComentarioFormulario()
    return render(request, "app_blog/crear_comentario.html", {"formulario": formulario})

@login_required
def editar_comentario(request, id):
    # Recibe param profesor id, con el que obtenemos el profesor
    comentario = Comentario.objects.get(id=id)

    if request.method == 'POST':
        formulario = ComentarioFormulario(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data

            comentario.nombre_usuario = data['nombre_usuario']
            comentario.comentario = data['comentario']
            comentario.id_usuario = data['id_usuario']
            comentario.post_id = data['post_id']

            comentario.save()

            return redirect(reverse('comentario'))
    else:
        inicial = {
            'nombre_usuario': comentario.nombre_usuario,
            'comentario': comentario.comentario,
            'id_usuario': comentario.id_usuario,
            'post_id': comentario.post_id,
        }
        formulario = ComentarioFormulario(initial=inicial)
    return render(request, "app_blog/crear_comentario.html", {"formulario": formulario})

@login_required
def eliminar_comentario(request, id):
    comentario = Comentario.objects.get(id=id)
    comentario.delete()
    return redirect(reverse('comentario'))    




# LOGIN 

def register(request):
    mensaje = ''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "app_blog/about.html", {"mensaje": "Usuario Creado :)"})
        else:
            mensaje = 'Cometiste un error en el registro'
    formulario = UserRegisterForm()  # Formulario vacio para construir el html
    context = {
        'form': formulario,
        'mensaje': mensaje
    }

    return render(request, "app_blog/registro.html", context=context)    

def login_request(request):
    next_url = request.GET.get('next')
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            usuario = form.cleaned_data.get('username')
            contra = form.cleaned_data.get('password')
            user = authenticate(username=usuario, password=contra)
            if user:
                login(request=request, user=user)
                if next_url:
                    return redirect(next_url)
                return render(request, "app_blog/about.html", {"mensaje":f"Bienvenido {usuario}"})
            else:
                return render(request,"app_blog/about.html", {"mensaje":"Error, datos incorrectos"})
        else:
            return render(request,"app_blog/about.html", {"mensaje":"Error, formulario erroneo"})

    form = AuthenticationForm()
    return render(request,"app_blog/login2.html", {'form':form} )


class CustomLogoutView(LogoutView):
    template_name = 'app_blog/logout.html'
    next_page = reverse_lazy('home')
