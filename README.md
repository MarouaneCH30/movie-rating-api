# Simple Movie Rating API (Django + DRF)

Small educational API to create movies, add 1–5 star ratings with optional reviews, and compute average ratings.

## Stack
- Django 5.x
- Django REST Framework

## Endpoints
- `GET /api/movies/` — list movies
- `POST /api/movies/` — create movie
- `GET /api/movies/<id>/` — movie details
- `GET /api/movies/<id>/ratings/` — list ratings for a movie
- `POST /api/movies/<id>/ratings/` — add rating/review
- `GET /api/movies/<id>/average/` — average rating

## Quickstart
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
