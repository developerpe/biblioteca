import pytest

from faker import Faker
from ddf import G, F

from apps.libro.models import Autor, Libro

fake = Faker()

@pytest.fixture
def create_libro():
    # forma 1
    autor_1 = G(Autor, )
    autor_2 = G(Autor)
    return G(Libro, autor=[autor_1, autor_2, F()])

    # forma 2
    # autores = [F(nombre=fake.last_name()), F(nombre=fake.first_name())]

    # forma 3
    # return G(Libro, autor=[F(nombre=fake.last_name()), F(nombre=fake.first_name())])

@pytest.mark.django_db
def test_create_libro(create_libro):
    print(create_libro.autor.all())
    assert create_libro.estado
