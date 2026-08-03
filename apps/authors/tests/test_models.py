import pytest
from apps.authors.models import Author
import uuid
from django.core.exceptions import ValidationError

@pytest.mark.django_db
def test_author_has_uuid():
    author = Author.objects.create(
        first_name="Manoj"
    )

    assert author.id is not None
    assert isinstance(author.id, uuid.UUID)


@pytest.mark.django_db
def test_create_author():
    author = Author.objects.create(
        first_name = "Manoj",
        last_name = "Pun"
    )

    assert author.first_name == "Manoj"
    assert author.last_name == "Pun"
    assert str(author) == "Manoj Pun"


@pytest.mark.django_db
def test_create_author_without_last_name():
    author = Author.objects.create(
        first_name = "Manoj"
    )

    assert author.first_name == "Manoj"
    assert author.last_name in ("",None)
    assert author.last_name == ""


@pytest.mark.django_db
def test_author_requires_first_name():
    with pytest.raises(ValidationError):
        Author(last_name="Pun").full_clean()


@pytest.mark.django_db
def test_author_ordering():
    Author.objects.create(first_name="Zack")
    Author.objects.create(first_name="Adam")

    authors = Author.objects.all()

    assert authors[0].first_name == "Adam"
