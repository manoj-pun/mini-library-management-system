# API Documentation — Mini Library Management System

Complete reference and walkthrough of every endpoint, with real example
requests and responses, in the order they'd naturally be used.

All endpoints (except login/register) require a JWT access token in the header:
---

## Endpoint Reference

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/token/` | Log in (get access + refresh tokens) |
| POST | `/api/token/refresh/` | Refresh an expired access token |

### Authors
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/authors/` | Librarian |
| GET | `/api/authors/{id}/` | Librarian |
| POST | `/api/authors/` | Librarian |
| PUT/PATCH | `/api/authors/{id}/` | Librarian |
| DELETE | `/api/authors/{id}/` | Librarian |

### Books
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/books/` | Any authenticated user |
| GET | `/api/books/{id}/` | Librarian |
| POST | `/api/books/` | Librarian |
| PUT/PATCH | `/api/books/{id}/` | Librarian |
| DELETE | `/api/books/{id}/` | Librarian |

### Members
| Method | Endpoint | Permission |
|--------|----------|------------|
| POST | `/api/members/` | Librarian |
| GET | `/api/members/` | Librarian |
| GET | `/api/members/{id}/` | Librarian |
| PATCH | `/api/members/{id}/` | Librarian |
| GET | `/api/members/me/` | Member (own profile) |
| POST | `/api/members/{id}/suspend/` | Librarian |
| POST | `/api/members/{id}/reactivate/` | Librarian |

### Borrowings
| Method | Endpoint | Permission |
|--------|----------|------------|
| GET | `/api/borrowings/` | Own records (Member) / all records (Librarian) |
| GET | `/api/borrowings/{id}/` | Own record (Member) / any (Librarian) |
| POST | `/api/borrowings/borrow/` | Member |
| POST | `/api/borrowings/{id}/return/` | Member |
| POST | `/api/borrowings/{id}/pay-fine/` | Librarian |

---

## Step-by-Step Walkthrough

### 1. Log in as librarian
```http
POST /api/token/
Content-Type: application/json

{
    "email": "librarian@example.com",
    "password": "your-superuser-password"
}
```
**Response** (200 OK)
```json
{
    "refresh": "eyJhbGciOi...",
    "access": "eyJhbGciOi..."
}
```

Use the `access` token as `Authorization: Bearer <access_token>` for every request below.

---

### 2. Create an author (librarian)
```http
POST /api/authors/
Authorization: Bearer <librarian_token>

{
  "first_name": "George",
  "last_name": "Orwell",
  "birth_date": "1903-06-25"
}
```
**Response** (201 Created)
```json
{
    "id": "3f1a9c2e-4b5d-4a6f-8e9d-0a1b2c3d4e5f",
    "first_name": "George",
    "last_name": "Orwell",
    "birth_date": "1903-06-25"
}
```
---

### 3. List authors (librarian)
```http
GET /api/authors/
Authorization: Bearer <librarian_token>
```

**Response** (201 Created)
```json
{
    "count": 6,
    "next": "http://localhost:8000/api/authors/?page=2",
    "previous": null,
    "results": [
        {
            "id": "d7bb65ee-df05-4563-b7bf-e9751a835ffd",
            "first_name": "Evelyn",
            "last_name": "Waugh",
            "birth_date": "1993-12-02"
        },
        {
            "id": "f80549de-7ec7-4a3d-910d-d0a63ff8f994",
            "first_name": "George",
            "last_name": "Orwell",
            "birth_date": "1903-06-25"
        }
    ]
}
```

---

### 4. List author with id 
```http
GET /api/authors/f80549de-7ec7-4a3d-910d-d0a63ff8f994/
Authorization: Bearer <librarian_token>
```

**Response** (200 0K)
```json
{
    "id": "f80549de-7ec7-4a3d-910d-d0a63ff8f994",
    "first_name": "George",
    "last_name": "Orwell",
    "birth_date": "1903-06-25",
    "created_at": "2026-07-23T10:57:06.497892Z",
    "updated_at": "2026-07-23T10:57:06.497910Z"
}
```

---
### 5. List author with search
```http
GET /api/authors/?search=Orwell
Authorization: Bearer <librarian_token>
```

**Response** (200 OK)
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "f80549de-7ec7-4a3d-910d-d0a63ff8f994",
            "first_name": "George",
            "last_name": "Orwell",
            "birth_date": "1903-06-25"
        }
    ]
}
```
---
### 6. Update authors
```http
PUT/PATCH /api/authors/f80549de-7ec7-4a3d-910d-d0a63ff8f994/
Authorization: Bearer <librarian_token>
{
    "last_name":"Updated"
}
```
**Response** (200 OK)
```json
{
    "first_name": "George",
    "last_name": "Updated",
    "birth_date": "1903-06-25"
}
```
---
### 7. Delete authors
```http
DELETE /api/authors/f80549de-7ec7-4a3d-910d-d0a63ff8f994/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
```
---
### 8. Create books
```http
POST /api/books/
Authorization: Bearer <librarian_token>
{
    "title": "Design Patterns",
    "authors": [
        "25a88f8d-b64a-40b4-bc1b-24742d77ac59",
        "d7bb65ee-df05-4563-b7bf-e9751a835ffd",
        "b664f4ce-febb-4008-9723-0550b282e22b"
    ],
    "isbn": "9780201633610",
    "genre": "Software Engineering",
    "published_date": "1994-10-21",
    "total_copies": 3
}
```
**Response** (201 CREATED)
```json
{
    "title": "Design Patterns",
    "authors": [
        "d7bb65ee-df05-4563-b7bf-e9751a835ffd",
        "b664f4ce-febb-4008-9723-0550b282e22b",
        "25a88f8d-b64a-40b4-bc1b-24742d77ac59"
    ],
    "isbn": "9780201633610",
    "genre": "Software Engineering",
    "published_date": "1994-10-21",
    "total_copies": 3
}
```
---
### 9. List books
```http
GET /api/books/
Authorization: Bearer <librarian_token>
or
Authorization: Bearer <member_token>
```
**Response** (200 OK)
```json
{
    "count": 6,
    "next": "http://localhost:8000/api/books/?page=3",
    "previous": "http://localhost:8000/api/books/",
    "results": [
        {
            "id": "916e77d7-9738-471d-b114-1d69542fbf5a",
            "title": "Clean Code",
            "isbn": "9780132350884",
            "authors": [
                {
                    "first_name": "Isabel",
                    "last_name": "Allende"
                },
                {
                    "first_name": "Toni",
                    "last_name": "Morrison"
                }
            ],
            "available_copies": 0
        },
        {
            "id": "454e5aa3-3a08-4863-8a7d-5fabfe2061ad",
            "title": "Design Patterns",
            "isbn": "9780201633610",
            "authors": [
                {
                    "first_name": "Evelyn",
                    "last_name": "Waugh"
                },
                {
                    "first_name": "Haruki",
                    "last_name": "Murakami"
                },
                {
                    "first_name": "Truman",
                    "last_name": "Capote"
                }
            ],
            "available_copies": 3
        }
    ]
}
```
---
### 10. List book with id
```http
GET /api/books/916e77d7-9738-471d-b114-1d69542fbf5a/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
{
    "id": "916e77d7-9738-471d-b114-1d69542fbf5a",
    "title": "Clean Code",
    "isbn": "9780132350884",
    "authors": [
        {
            "id": "c18c6f84-9c87-4224-97fa-00de4e10311d",
            "first_name": "Isabel",
            "last_name": "Allende"
        },
        {
            "id": "652d13b0-8e35-48dd-a404-675bc10a5be5",
            "first_name": "Toni",
            "last_name": "Morrison"
        }
    ],
    "genre": "Programming",
    "published_date": "2008-08-01",
    "total_copies": 2,
    "available_copies": 2,
    "created_at": "2026-07-19T10:01:20.935637Z"
}
```
---
### 11. Search book
```http
GET /api/books/?search=clean
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "916e77d7-9738-471d-b114-1d69542fbf5a",
            "title": "Clean Code",
            "isbn": "9780132350884",
            "authors": [
                {
                    "first_name": "Isabel",
                    "last_name": "Allende"
                },
                {
                    "first_name": "Toni",
                    "last_name": "Morrison"
                }
            ],
            "available_copies": 0
        }
    ]
}
```
---
### 12. Ordering book
```http
GET /api/books/?ordering=title
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
{
    "count": 6,
    "next": "http://localhost:8000/api/books/?ordering=title&page=2",
    "previous": null,
    "results": [
        {
            "id": "afbe0402-c718-4cb3-8f3b-0cc6b983b409",
            "title": "1984",
            "isbn": "9780451524935",
            "authors": [
                {
                    "first_name": "Evelyn",
                    "last_name": "Waugh"
                }
            ],
            "available_copies": 5
        },
        {
            "id": "e5e79675-81d2-482b-a1ba-9cff45e7d97f",
            "title": "Animal Farm",
            "isbn": "9780451526342",
            "authors": [
                {
                    "first_name": "Haruki",
                    "last_name": "Murakami"
                }
            ],
            "available_copies": 4
        }
    ]
}
```
---
### 13. Update books
```http
PUT/PATCH /api/books/916e77d7-9738-471d-b114-1d69542fbf5a/
Authorization: Bearer <librarian_token>
{
    "total_copies":"2"
}
```
**Response** (200 OK)
```json
{
    "title": "Clean Code",
    "authors": [
        "c18c6f84-9c87-4224-97fa-00de4e10311d",
        "652d13b0-8e35-48dd-a404-675bc10a5be5"
    ],
    "isbn": "9780132350884",
    "genre": "Programming",
    "published_date": "2008-08-01",
    "total_copies": 2
}
```
---
### 14.  Deleting book
```http
DELETE /api/books/916e77d7-9738-471d-b114-1d69542fbf5a/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
```
---

### 15. Create members
```http
POST/api/members/
Authorization: Bearer <librarian_token>
{
    "first_name":"Member",
    "last_name":"Pun",
    "email":"member3@gmail.com",
    "password" :"12345678",
    "phone_number":"9800000000"
}
```
**Response** (200 CREATED)
```json
{
    "id": "62fbbb64-477b-4681-aa2a-5b77ccc7567d",
    "first_name": "Member",
    "last_name": "Pun",
    "email": "member3@gmail.com",
    "membership_number": "MEM-00002",
    "phone_number": "9800000000",
    "address": "",
    "status": "ACTIVE",
    "joined_date": "2026-07-23"
}
```
---

### 16. List all members
```http
GET /api/members/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "62fbbb64-477b-4681-aa2a-5b77ccc7567d",
            "first_name": "Member",
            "membership_number": "MEM-00002",
            "phone_number": "9800000000"
        },
        {
            "id": "bfadecfe-3864-4cf4-a1b3-348a904a617a",
            "first_name": "Member",
            "membership_number": "MEM-00001",
            "phone_number": "9800000000"
        }
    ]
}
```
---
### 17. List member with id
```http
GET /api/members/dad1c082-afad-4c7d-8e76-6db60e8752ac/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
{
    "id": "dad1c082-afad-4c7d-8e76-6db60e8752ac",
    "first_name": "Updated",
    "last_name": "Pun",
    "email": "member2@gmail.com",
    "membership_number": "MEM-00002",
    "phone_number": "9800000000",
    "address": "",
    "status": "ACTIVE",
    "joined_date": "2026-07-21"
}
```
---
### 18. Update member
```http
PUT/PATCH /api/members/dad1c082-afad-4c7d-8e76-6db60e8752ac/
Authorization: Bearer <librarian_token>
{
    "first_name":"Updated"
}
```
**Response** (200 OK)
```json
{
    "phone_number": "9800000000",
    "address": ""
}
```
---
### 19. Suspend member
```http
POST /api/members/bfadecfe-3864-4cf4-a1b3-348a904a617a/suspend/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
```
---
### 20. Reactivate member
```http
POST /api/members/bfadecfe-3864-4cf4-a1b3-348a904a617a/reactivate/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
```
---
### 21. Login member
```http
POST /api/token/
Authorization: Bearer <librarian_token>
{
    "email": "member@gmail.com",
    "password": "12345678"
}
```
**Response** (200 OK)
```json
{
    "refresh": "eyJhbGciOi.....",
    "access": "eyJhbGciOi....."
}
```
---
### 22.  Borrow books
```http
POST /api/borrowings/borrow/
Authorization: Bearer <member_token>
{
    "book":"916e77d7-9738-471d-b114-1d69542fbf5a"
}
```
**Response** (201 CREATED)
```json
{
    "id": "edc5208b-5b5f-489b-917c-42ef73f02bfc",
    "membership_number": "MEM-00001",
    "book": "916e77d7-9738-471d-b114-1d69542fbf5a",
    "borrowed_date": "2026-07-22",
    "due_date": "2026-08-11",
    "returned_date": null,
    "status": "BORROWED",
    "is_overdue": false,
    "days_overdue": 0,
    "fine_amount": "0.00",
    "fine_paid": false
}
```
---
### 23. Return book
```http
POST /api/borrowings/874e80fb-4ba8-4ab8-958b-e6ec0457a9f2/return/
Authorization: Bearer <member_token>
```
**Response** (200 OK)
```json
{
    "id": "874e80fb-4ba8-4ab8-958b-e6ec0457a9f2",
    "membership_number": "MEM-00001",
    "book": "916e77d7-9738-471d-b114-1d69542fbf5a",
    "borrowed_date": "2026-07-22",
    "due_date": "2026-08-11",
    "returned_date": "2026-07-22",
    "status": "RETURNED",
    "is_overdue": false,
    "days_overdue": 0,
    "fine_amount": "0.00",
    "fine_paid": false
}
```
---
### 24. Pay fine
```http
POST /api/borrowings/874e80fb-4ba8-4ab8-958b-e6ec0457a9f2/pay-fine/
Authorization: Bearer <librarian_token>
```
**Response** (200 OK)
```json
```
---

