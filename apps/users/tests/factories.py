import factory
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = User.Role.MEMBER

    password = factory.PostGenerationMethodCall(
        "set_password",
        "password123"
    )