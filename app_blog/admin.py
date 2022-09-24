from django.contrib import admin

# Register your models here.
from app_blog.models import *

admin.site.register(Usuario)
admin.site.register(Post)
admin.site.register(Comentario)