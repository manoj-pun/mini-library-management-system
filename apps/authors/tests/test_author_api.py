import pytest
from apps.authors.models import Author

@pytest.mark.django_db
def test_only_librarian_can_create_author(api_client, librarian_user):
    api_client.force_authenticate(user=librarian_user)

    response = api_client.post(
        "/api/authors/",
        {
            "first_name": "manoj",
            "last_name": "pun"
        },
        format="json"
    )

    assert response.status_code == 201
    assert Author.objects.count() == 1
    assert Author.objects.first().first_name == "Manoj"


@pytest.mark.django_db
def test_non_librarian_cannot_create_author(api_client, member_user):
        api_client.force_authenticate(user=member_user)

        response = api_client.post(
            "/api/authors/",
            {
                "first_name": "Manoj",
                "last_name": "Pun"
            },
            format="json"
        )

        assert response.status_code == 403
        assert Author.objects.count() == 0


@pytest.mark.django_db
def test_anonymous_user_cannot_create_author(api_client):
        response = api_client.post(
            "/api/authors/",
            {
                "first_name": "Manoj",
                "last_name": "Pun"
            },
            format="json"
        )

        assert response.status_code in [401, 403]


@pytest.mark.django_db
def test_only_librarian_can_list_authors(api_client, librarian_user):
        Author.objects.create(
            first_name="Manoj",
            last_name="Pun"
        )

        api_client.force_authenticate(user=librarian_user)

        response = api_client.get(
            "/api/authors/"
        )

        assert response.status_code == 200
        assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_only_librarian_can_retrieve_author(api_client,librarian_user):
        author = Author.objects.create(
            first_name="Manoj",
            last_name="Pun"
        )

        api_client.force_authenticate(user=librarian_user)

        response = api_client.get(
            f"/api/authors/{author.id}/"
        )

        assert response.status_code == 200
        assert response.data["first_name"] == "Manoj"


@pytest.mark.django_db
def test_only_librarian_can_update_author(api_client, librarian_user):
        author = Author.objects.create(
            first_name="Manoj",
            last_name="Pun"
        )

        api_client.force_authenticate(user=librarian_user)

        response = api_client.patch(
            f"/api/authors/{author.id}/",
            {
                "first_name": "eric"
            },
            format="json"
        )

        assert response.status_code == 200
        author.refresh_from_db()
        assert author.first_name == "Eric"


@pytest.mark.django_db
def test_non_librarian_cannot_update_author(api_client, member_user):
        author = Author.objects.create(
            first_name="George"
        )

        api_client.force_authenticate(user=member_user)

        response = api_client.patch(
            f"/api/authors/{author.id}/",
            {
                "first_name": "Eric"
            },
            format="json"
        )

        assert response.status_code == 403


@pytest.mark.django_db
def test_only_librarian_can_delete_author(api_client, librarian_user):
        author = Author.objects.create(
            first_name="Manoj"
        )

        api_client.force_authenticate(user=librarian_user)

        response = api_client.delete(
            f"/api/authors/{author.id}/"
        )

        assert response.status_code == 204
        assert Author.objects.count() == 0


@pytest.mark.django_db
def test_search_authors(api_client, librarian_user):
    Author.objects.create(
        first_name="Manoj",
        last_name="Pun"
    )

    Author.objects.create(
        first_name="John",
        last_name="Doe"
    )

    api_client.force_authenticate(user=librarian_user)

    response = api_client.get(
        "/api/authors/?search=Manoj"
    )

    assert response.status_code == 200
    assert len(response.data["results"]) == 1