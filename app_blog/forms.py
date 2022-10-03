from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_blog.models import *
from ckeditor.widgets import CKEditorWidget

class UsuarioFormulario(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    nombre_usuario = forms.CharField(max_length=100)
    correo = forms.EmailField()

class PostFormulario(forms.Form):
    titulo = forms.CharField(max_length=50)
    subtitulo = forms.CharField(max_length=255)
    imagen = forms.ImageField()
    cuerpo = forms.CharField(widget=CKEditorWidget())
    autor = forms.CharField(max_length=50)


class ComentarioFormulario(forms.Form):
    nombre_usuario = forms.CharField(max_length=100)
    comentario = forms.CharField(widget=forms.Textarea)
    id_usuario = forms.ModelChoiceField(queryset=Usuario.objects.all())
    post_id = forms.ModelChoiceField(queryset=Post.objects.all())


class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class AvatarFormulario(forms.ModelForm):

    class Meta:
        model = Avatar
        fields = ['imagen']

class AvatarUpdateFormulario(forms.ModelForm):

    class Meta:
        model = Avatar
        fields = ['imagen']