from faker import Faker
from faker.providers import BaseProvider

fake = Faker()

class EmailProvider(BaseProvider):

  def custom_email(self):
      return f'{fake.last_name().lower()}@gmail.com' 