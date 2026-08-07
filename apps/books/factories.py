import factory
from apps.books.models import Book
from apps.authors.factories import AuthorFactory

class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
        skip_postgeneration_save = True

    title = factory.Faker("sentence", nb_words=3)
    isbn = factory.Sequence(lambda n: f"978000000{n:04d}")
    total_copies = 5
    available_copies = 5

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.authors.add(*extracted)
        else:
            self.authors.add(AuthorFactory())