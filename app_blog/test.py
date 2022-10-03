import random
import string

from django.test import TestCase
from app_blog.models import Usuario, Post, Comentario

class PostTestCase(TestCase):

    # User's tests #

    def test_create_users(self):

        """Test 1: We are going to check the correct operation of the "create user" module,
            we are going to try to create a new user and check if the information was stored in
            the data base."""

        Usuario(nombre="Juan",
                apellido="Manriquez",
                nombre_usuario="jmanriquez",
                correo="jmanriquez@test.com").save()

        users = Usuario.objects.first()
        self.assertEquals(users.correo, "jmanriquez@test.com")
        self.assertEquals(users.nombre_usuario, "jmanriquez")

    def test_edit_user(self):

        """Test 2: We are going to check the correct operation of the "edit user" module,
            we are going to try to modify the user information, we are going to midify
            the "nombre_usuario" field."""

        Usuario(nombre="Juan",
                apellido="Manriquez",
                nombre_usuario="jmanriquez",
                correo="jmanriquez@test.com").save()

        users = Usuario.objects.first()
        usuario = Usuario.objects.get(id=users.id)

        usuario.nombre_usuario = "jesus_manriquez"
        usuario.save()

        users = Usuario.objects.first()
        self.assertEquals(users.nombre_usuario, "jesus_manriquez")

    def test_delete_user(self):

        """Test 3: We are going to check the correct operation of the "delete user" module,
            we are going to try to create and delete an user."""

        Usuario(nombre="Juan",
                apellido="Manriquez",
                nombre_usuario="jmanriquez",
                correo="jmanriquez@test.com").save()

        users_count = Usuario.objects.all()
        self.assertEquals(users_count.count(), 1)

        users = Usuario.objects.first()
        usuario = Usuario.objects.get(id=users.id)

        usuario.delete()

        users_count = Usuario.objects.all()
        self.assertEquals(users_count.count(), 0)