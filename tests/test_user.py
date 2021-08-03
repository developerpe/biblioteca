import pytest

from apps.usuario.models import Usuario

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