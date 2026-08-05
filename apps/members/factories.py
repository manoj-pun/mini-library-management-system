import factory
from apps.users.factories import UserFactory
from apps.members.models import Member

class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory) #Before creating a Member, create a User.
    membership_number = factory.Sequence(lambda n: f"MEM-{n+1:05d}")
    phone_number = factory.Sequence(lambda n: f"98000000{n:02d}")
    address = factory.Faker("address")

