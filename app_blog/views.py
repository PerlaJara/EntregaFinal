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
    avatar = Avatar.objects.get(user_id=request.user)
    return render(request, "app_blog/base.html", {"avatar" : avatar})

def about(request):
    return render(request, "app_blog/about.html")

def blog(request):
    blogs = Post.objects.all()
    total = len(blogs)

    return render(request, "app_blog/inicio.html", {'blogs' : blogs, "total" : total })

### USERS SECTION ###

@login_required
def usuario(request):
    usuarios = User.objects.filter(is_staff=0, is_active=1)
    return render(request, "app_blog/usuarios.html", {'usuarios' : usuarios})

@login_required
def buscar_usuario_form(request):
    return render(request, "app_blog/buscar_usuario.html")

@login_required
def buscar_usuario(request):
    if request.GET["valor"]:
        valor = request.GET["valor"]
        usuario = User.objects.filter(first_name__icontains=valor) | User.objects.filter(last_name__icontains=valor) | User.objects.filter(username__icontains=valor)
        return render(request, "app_blog/usuarios.html", {'usuarios': usuario})
    else:
        return render(request, "app_blog/usuarios.html", {'usuarios': []})

def eliminar_usuario(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect(reverse('usuario'))

def profile(request):
    user = Usuario.objects.get()

def register(request):
    mensaje = ''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return render(request, "app_blog/about.html", {"mensaje": "Usuario Creado: )"})
        else:
            mensaje = 'Cometiste un error en el registro'
    formulario = UserRegisterForm()
    context = {
        'form': formulario,
        'mensaje': mensaje
    }

    return render(request, "app_blog/registro.html", context=context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('home')
    template_name = 'app_blog/form_perfil.html'

    def get_object(self, queryset=None):
        return self.request.user

#### POSTS SECTION ###

@login_required
def post(request):
    if request.user.is_superuser == 1:
        posts = Post.objects.all()
        return render(request, "app_blog/posts.html", {'posts' : posts})
    else:
        posts = Post.objects.filter(usuario_id_id=request.user.id)
        return render(request, "app_blog/posts.html", {'posts' : posts})

@login_required
def post_formulario(request):
    if request.method == 'POST':
        formulario= PostFormulario(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data
            post = Post(titulo=data['titulo'], subtitulo=data['subtitulo'], imagen=data['imagen'], cuerpo=data['cuerpo'], autor=data['autor'], usuario_id=request.user)
            post.save()
            return render(request, "app_blog/inicio.html", {"exitoso": True})
    else:
        formulario= PostFormulario()
    return render(request, "app_blog/crear_post.html", {"formulario": formulario, "title" : "Crear Post"})

@login_required
def editar_post(request, id):
    post = Post.objects.get(id=id)

    if request.method == 'POST':
        formulario = PostFormulario(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data

            print("IMPRIMIENDO INFORMACIÓN LIMPIA")
            print(data)

            post.titulo = data['titulo']
            post.subtitulo = data['subtitulo']
            post.imagen = data['imagen']
            post.cuerpo = data['cuerpo']
            post.autor = data['autor']
            post.usuario_id = User.objects.get(id=request.user.id)

            print('IMPRIMIENDO CONTENIDO DE POST')
            print(post)

            post.save()

            return redirect(reverse('post'))
    else:
        print('ENTRANDO AL ERROR DEL POST')
        inicial = {
            'titulo': post.titulo,
            'subtitulo': post.subtitulo,
            'imagen': post.imagen,
            'cuerpo': post.cuerpo,
            'autor': post.autor,
        }
        formulario = PostFormulario(initial=inicial)
    return render(request, "app_blog/crear_post.html", {"formulario": formulario, "title" : "Editar Post"})

@login_required
def eliminar_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect(reverse('post'))

def show_post(request, id):
    post = Post.objects.get(id=id)
    return render(request, "app_blog/show_post.html", {"post": post})


### COMENTS SECTION ###

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

### AVATAR SECTION ###

@login_required
def agregar_avatar(request):
    if request.method == 'POST':

        form = AvatarFormulario(request.POST, request.FILES)

        if form.is_valid:
            avatar = form.save()
            avatar.user = User.objects.get(id=request.user.id)
            avatar.save()
            return redirect(reverse('home'))

    form = AvatarFormulario()
    return render(request, "app_blog/form_avatar.html", {"form":form})

@login_required
def avatar_update(request):
    avatar = Avatar.objects.get(user_id=request.user)

    if request.method == 'POST':
        formulario = AvatarFormulario(request.POST, request.FILES)

        if formulario.is_valid():
            data = formulario.cleaned_data
            avatar.imagen = data['imagen']
            avatar.user_id = request.user.id
            avatar.save()
            return redirect(reverse('home'))
    else:
        form = AvatarFormulario()
        return render(request, "app_blog/form_avatar.html", {"form":form})


### LOGIN SECTION ###

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
    return render(request,"app_blog/login.html", {'form':form} )


class CustomLogoutView(LogoutView):
    template_name = 'app_blog/logout.html'
    next_page = reverse_lazy('home')