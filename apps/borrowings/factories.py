import factory

from datetime import timedelta
from django.utils import timezone
from apps.borrowings.models import Borrowing
from apps.books.factories import BookFactory
from apps.members.factories import MemberFactory


class BorrowingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Borrowing

    member = factory.SubFactory(MemberFactory)
    book = factory.SubFactory(BookFactory)
    due_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=20))
    status = Borrowing.BorrowStatus.BORROWED