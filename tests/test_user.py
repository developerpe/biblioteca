import pytest

from faker import Faker
from ddf import G, N, F

from tests.providers.general_providers import EmailProvider
from apps.usuario.models import Usuario, Rol

fake = Faker()
fake.add_provider(EmailProvider)

@pytest.fixture
def user_creation():
    rol = G(Rol)
    return N(Usuario, rol=rol)

@pytest.mark.django_db
def test_common_user_creation(user_creation):
    assert user_creation.is_staff == False

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