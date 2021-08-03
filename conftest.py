import pytest

from tests.factories import UsuarioAdminFactory

from apps.usuario.models import Usuario, Rol

@pytest.fixture
def user_creation():
    return UsuarioAdminFactory.create()