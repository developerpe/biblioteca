import pytest

from apps.usuario.models import Usuario

@pytest.mark.django_db
def test_common_user_creation():
    user = Usuario.objects.create_user(
            username='dasdas',
            email='asdasda@gmail.com',
            nombres='wegw gwgwe',
            password='12345',
            is_staff=False
    )
    assert user.username == 'dasdas'

@pytest.mark.django_db
def test_superuser_creation():
    user = Usuario.objects.create_superuser(
            username='dasdas',
            email='asdasda@gmail.com',
            nombres='wegw gwgwe',
            password='12345'
    )

    assert user.is_superuser

@pytest.mark.django_db
def test_staff_user_creation():
    user = Usuario.objects.create_user(
            username='dasdas',
            email='asdasda@gmail.com',
            nombres='wegw gwgwe',
            password='12345',
            is_staff=False
    )

    assert user.is_staff