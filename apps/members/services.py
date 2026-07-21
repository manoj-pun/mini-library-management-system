from django.db import transaction
from apps.users.models import User
from apps.members.models import Member

def generate_membership_number():

    """
    Function to generate membership number.
    select_for_update() for preventing race condition.
    """

    last = (Member.objects.select_for_update().order_by("-joined_date").first())

    next_number = (1 if not last else int(last.membership_number.split("-")[1]) + 1)

    return f"MEM-{next_number:05d}"


@transaction.atomic
def create_member(*, first_name, last_name, email, password, phone_number, address=""):

    """
    Function to create users and create members based on that user data.
    """

    user = User.objects.create_user(
        first_name = first_name,
        last_name = last_name,
        email = email,
        password = password,
        role = User.Role.MEMBER
    )

    member = Member.objects.create(
        user = user,
        membership_number=generate_membership_number(),
        phone_number = phone_number,
        address = address
    )

    return member


##Suspend user 