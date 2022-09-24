from django.urls import path

from app_blog import views

urlpatterns = [
    #Main URL
    path('', views.blog, name="home"),

    #URL's user
    path('usuario/', views.usuario, name="usuario"),
    path('crear_usuario/', views.usuario_formulario, name="crear_usuario"),
    path('editar_usuario/<int:id>/', views.editar_usuario, name="editar_usuario"),
    path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name="eliminar_usuario"),
    path('buscar_usuario_form/', views.buscar_usuario_form, name="buscar_usuario_form"),
    path('buscar_usuario/', views.buscar_usuario, name="buscar_usuario"),

    #URL's post
    path('post/', views.post, name="post"),
    path('crear_post/', views.post_formulario, name="crear_post"),
    path('editar_post/<int:id>/', views.editar_post, name="editar_post"),
    path('eliminar_post/<int:id>/', views.eliminar_post, name="eliminar_post"),

    #URL's comentario
    path('comentario/', views.comentario, name="comentario"),
    path('crear_comentario/', views.comentario_formulario, name="crear_comentario"),

    #URL's about
    path('about/', views.about, name="about"),

    #URL's my account
    path('login/', views.login, name="login"),
]