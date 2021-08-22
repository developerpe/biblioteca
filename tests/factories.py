import factory
from faker import Faker

from tests.providers.general_providers import EmailProvider
from apps.usuario.models import Usuario, Rol

fake = Faker()
fake.add_provider(EmailProvider)

class RolFactory(factory.Factory):
    class Meta:
        model = Rol

    rol = 'admin'

class UsuarioComunFactory(factory.Factory):
    class Meta:
        model = Usuario
    
    nombres = "Oliver"
    username = "oliver"
    email = fake.email()
    is_staff = False

class UsuarioAdminFactory(factory.Factory):
    class Meta:
        model = Usuario
    
    nombres = "Oliver"
    username = "oliver"
    is_staff = True
    is_superuser = True
    #rol = factory.SubFactory(RolFactory)

class UsuarioStaffFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario

    nombres = "Oliver"
    username = "oliver"
    email = fake.email()
    is_staff = True