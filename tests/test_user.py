import pytest

from apps.usuario.models import Usuario

@pytest.fixture
def user_creation():
    return Usuario(
                username='kjbkwejfw',
                email='asdasd@gmail.com',
                nombres='sadasd fasfas',
                password='12345'
            )

@pytest.mark.django_db
def test_common_user_creation(user_creation):
    user_creation.is_staff = False
    user_creation.save()
    assert user_creation.is_staff == False

@pytest.mark.django_db
def test_superuser_creation(user_creation):
    user_creation.is_superuser = True
    user_creation.is_staff = True
    user_creation.save()
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