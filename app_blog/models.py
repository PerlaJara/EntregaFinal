from datetime import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nombre_usuario = models.CharField(max_length=100)
    correo = models.EmailField()
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}, {self.nombre_usuario}'


class Post(models.Model):
    titulo = models.CharField(max_length=50)
    subtitulo = models.CharField(max_length=250)
    imagen = models.ImageField( null=True, blank = True, upload_to='posts')
    cuerpo = RichTextField(blank=True, null=True)
    autor = models.CharField(max_length=50)
    fecha_creacion = models.DateField(auto_now_add=True)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}, {self.titulo}'


class Comentario(models.Model):
    nombre_usuario = models.CharField(max_length=100)
    comentario = models.TextField()
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey('Post', on_delete=models.CASCADE)


class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    imagen = models.ImageField(upload_to='avatares', null=True, blank = True)

    def __str__(self):
        return f"Imagen de: {self.user}"