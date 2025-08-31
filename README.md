Simple Movie Review API — Quick API Guide

Base URL (local): http://127.0.0.1:8000
Content-Type: application/json
Auth header (after login):
Authorization: Token YOUR_TOKEN_HERE
0) Run locally (quick)
# activate venv, install, migrate, run
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
(Optional admin user for creating platforms/movies)
python manage.py createsuperuser
1) Accounts (Auth)
Register

POST /api/account/register/
Body:
{
  "username": "maro",
  "email": "maro@example.com",
  "password": "pass1234",
  "password2": "pass1234"
}
201 Created → returns token + basic user info.

Login (get token)

POST /api/account/login/
Body:
{
  "username": "maro",
  "password": "pass1234"
}
Logout

POST /api/account/logout/
Headers:

Authorization: Token YOUR_TOKEN_HERE
2) Stream Platforms (Admin-only to create/update/delete)
Create platform

POST /api/watch/stream/
Headers: Authorization: Token ADMIN_TOKEN
Body:

{
  "name": "Netflix",
  "about": "Streaming platform",
  "website": "https://netflix.com"
}


201 Created

List platforms

GET /api/watch/stream/
200 OK

Retrieve / Update / Delete platform

GET /api/watch/stream/<platform_id>/
PUT/PATCH/DELETE /api/watch/stream/<platform_id>/
(Updates/deletes require admin token)

3) Movies / Watch List (Admin-only to create/update/delete)
Create movie

POST /api/watch/
Headers: Authorization: Token ADMIN_TOKEN
Body:

{
  "title": "The Dark Knight",
  "storyline": "Batman faces the Joker in Gotham City.",
  "platform": 1,
  "active": true
}


201 Created

List movies

GET /api/watch/
200 OK

Movie detail / update / delete

GET /api/watch/<movie_id>/
PUT/PATCH/DELETE /api/watch/<movie_id>/ (admin token required for write)

4) Reviews (User CRUD; owner-only edit/delete)
Create a review for a movie

POST /api/watch/<movie_id>/reviews/create/
Headers: Authorization: Token USER_TOKEN
Body:

{
  "rating": 5,
  "description": "Absolute banger."
}


201 Created
(If same user reviews same movie twice → 400 with validation error)

List reviews for a movie

GET /api/watch/<movie_id>/reviews/
200 OK (paginated)

Review detail / update / delete (owner-only)

GET /api/watch/reviews/<review_id>/
PATCH /api/watch/reviews/<review_id>/
Body (example):

{ "rating": 4 }


DELETE /api/watch/reviews/<review_id>/

Owner editing/deleting → allowed

Non-owner → 403 Forbidden

User’s reviews (by username)

GET /api/watch/user-reviews/?username=maro
200 OK

5) Filtering, Search, Ordering, Pagination (on reviews list)

All apply to: GET /api/watch/<movie_id>/reviews/

Pagination (DRF default):

/api/watch/1/reviews/?page=1


Filter by rating:

/api/watch/1/reviews/?rating=5


Filter by username:

/api/watch/1/reviews/?review_user__username=maro


Search (in description):

/api/watch/1/reviews/?search=banger


Ordering:

/api/watch/1/reviews/?ordering=-created   # newest first
/api/watch/1/reviews/?ordering=rating     # lowest rating first


If your Review model uses created_at instead of created, use ?ordering=-created_at.
6) Common Responses

401 Unauthorized — missing or invalid token
→ Add header Authorization: Token YOUR_TOKEN_HERE

403 Forbidden — permissions block (e.g., non-admin creating movie; editing someone else’s review)

404 Not Found — wrong IDs/URLs

400 Bad Request — serializer validation failed (e.g., rating out of 1–5, duplicate review)