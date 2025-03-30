import factory
from django.contrib.auth.hashers import make_password
from faker import Faker

from .models import User

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = User

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.password = make_password(extracted)
        self.save()
