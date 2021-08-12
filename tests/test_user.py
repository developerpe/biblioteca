import pytest

from django.test import TestCase

from apps.usuario.models import Usuario
from tests.factories import UsuarioAdminFactory, UsuarioComunFactory

"""
@pytest.mark.django_db
def test_common_user_creation(user_creation):
    print(user_creation.rol)
    assert True

@pytest.mark.django_db
def test_superuser_creation(user_creation):
    user_creation.is_superuser = True
    user_creation.is_staff = True
    assert user_creation.is_superuser

@pytest.mark.django_db
def test_staff_user_creation(user_creation):
    user_creation.is_staff = True
    assert user_creation.is_staff

@pytest.mark.django_db
def test_user_creation_fail():
    with pytest.raises(Exception):  
        Usuario.objects.create_user(
                password='12345',
                is_staff=False
        )
"""

class UsuarioTestCase(TestCase):

    def setUp(self):
        self.common_user = UsuarioComunFactory.create()
        self.superuser = UsuarioAdminFactory.create()
    
    def test_common_user_creation(self):
        self.assertEqual(self.common_user.is_active, True)
        self.assertEqual(self.common_user.is_staff, False)
        self.assertEqual(self.common_user.is_superuser, False)
    
    def test_suerpuser_creation(self):
        self.assertEqual(self.superuser.is_staff, True)
        self.assertEqual(self.superuser.is_superuser, True)