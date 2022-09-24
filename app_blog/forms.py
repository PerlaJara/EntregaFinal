from dataclasses import field
from django import forms
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
    usuario_id = forms.ModelChoiceField(queryset=Usuario.objects.all())

class ComentarioFormulario(forms.Form):
    nombre_usuario = forms.CharField(max_length=100)
    comentario = forms.CharField(widget=forms.Textarea)
    id_usuario = forms.ModelChoiceField(queryset=Usuario.objects.all())
    post_id = forms.ModelChoiceField(queryset=Post.objects.all())
