import factory
from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    role = User.Role.MEMBER

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "password123"
        self.set_password(password)

        if create:
            self.save(update_fields=["password"])