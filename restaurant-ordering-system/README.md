# HappyMeal Restaurant Ordering System

HappyMeal is a Django restaurant ordering system built for customers to browse meals, add menu items to a cart, place orders, and track order history. Staff users can manage the menu, categories, uploaded images, stock, and order status from protected staff pages.

The project also includes a Django REST Framework API, token/JWT authentication, Postman-ready endpoints, deployment settings, and a dark restaurant-style UI.

## What Was Done

- Built a restaurant website with home, menu, category, about, cart, checkout, order history, and order detail pages.
- Added user registration, login, logout, password reset, and login-required ordering.
- Added a 5-minute cooldown after 5 failed sign-in attempts for the website login and API token endpoints.
- Added staff-only dashboard access for menu, category, and order management.
- Added menu item image uploads, stock tracking, availability status, and category grouping.
- Added creator tracking for API-created menu items with `created_by`.
- Added creator-only API update/delete rules for menu items.
- Added paginated API menu item results with 6 items per page.
- Added API filtering by category and availability, search by name, and ordering by price.
- Added separate single-token and JWT authentication endpoints.
- Added CORS support for API testing.
- Added `api_docs.md` with endpoint documentation.
- Added `HappyMeal_API.postman_collection.json` for Postman testing.
- Added `.env`-based configuration with `python-decouple`.
- Added `dj-database-url` so SQLite works locally and PostgreSQL can be used for deployment.
- Added WhiteNoise static-file support and `collectstatic`.
- Added Waitress support for local Windows server testing.
- Added a `Procfile` for Gunicorn deployment.
- Added focused tests for website flows, API auth, menu item management, categories, cart, checkout, and orders.
- Updated the visual style with dark smoky-brown panels, gold borders, warm text, and styled menu/edit pages.

## Main Features

| Area | What It Does |
| --- | --- |
| Customers | Browse menu items, register, sign in, add to cart, checkout, and view orders. |
| Staff | Manage menu items, categories, images, stock, availability, and order status. |
| API | List, create, view, update, and delete menu items with auth rules. |
| Security | CSRF-protected forms, staff-only pages, creator-only API edits, and sign-in cooldown. |
| Deployment | Environment variables, database URL config, WhiteNoise, Waitress, Gunicorn, and requirements file. |

## Tech Stack

- Python
- Django
- Django REST Framework
- SQLite for local development
- PostgreSQL-ready database configuration
- DRF Token Authentication
- Simple JWT
- django-filter
- django-cors-headers
- python-decouple
- dj-database-url
- WhiteNoise
- Waitress
- Gunicorn
- Bootstrap
- Pillow

## Project Structure

```text
restaurant-ordering-system/
|-- happymeal/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- restaurants/
|   |-- auth_rate_limit.py
|   |-- auth_views.py
|   |-- forms.py
|   |-- models.py
|   |-- pagination.py
|   |-- permissions.py
|   |-- serializers.py
|   |-- test_api.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- static/
|   `-- templates/
|-- orders/
|-- media/
|-- staticfiles/
|-- api_docs.md
|-- HappyMeal_API.postman_collection.json
|-- Procfile
|-- requirements.txt
|-- manage.py
`-- README.md
```

## Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

For deployment, use a strong secret key, set `DEBUG=False`, set the real host in `ALLOWED_HOSTS`, and use a PostgreSQL `DATABASE_URL`.

The `.env` file should stay private and is ignored by Git.

## Setup

From the project folder:

```powershell
cd C:\Users\ogbon\OneDrive\Desktop\dune-cohort-final-project\restaurant-ordering-system
```

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Apply migrations:

```powershell
python manage.py migrate
```

Create a staff/admin account:

```powershell
python manage.py createsuperuser
```

Run the local Django server:

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Testing With Waitress On Windows

Waitress can be used to test the deployed-style WSGI server locally:

```powershell
python -m waitress --listen=127.0.0.1:8080 happymeal.wsgi:application
```

Open:

```text
http://127.0.0.1:8080/
```

If `DEBUG=False`, run `collectstatic` before testing static files:

```powershell
python manage.py collectstatic --noinput
```

## Important Website Routes

| URL | Purpose |
| --- | --- |
| `/` | Home page |
| `/about/` | About page |
| `/menu_list/` | Public menu listing |
| `/menu/<id>/` | Public menu item detail |
| `/categories/` | Category listing |
| `/cart/` | Cart page |
| `/checkout/` | Checkout page |
| `/orders/` | Customer order history |
| `/orders/<id>/` | Customer order detail |
| `/dashboard/` | Staff dashboard |
| `/menu-items/add/` | Add menu item |
| `/menu-items/<id>/edit/` | Edit menu item |
| `/menu-items/<id>/delete/` | Delete menu item |
| `/admin/` | Django admin |

## API Routes

| Method | URL | Auth Required | Purpose |
| --- | --- | --- | --- |
| `POST` | `/api/auth-token/` | No | Get one DRF auth token. |
| `POST` | `/api/token/` | No | Get JWT access and refresh tokens. |
| `POST` | `/api/token/refresh/` | No | Refresh a JWT access token. |
| `GET` | `/api/menu-items/` | No | List paginated menu items. |
| `POST` | `/api/menu-items/` | Yes | Create a menu item. |
| `GET` | `/api/menu-items/<id>/` | No | Retrieve one menu item. |
| `PUT` | `/api/menu-items/<id>/` | Yes | Update a menu item created by the authenticated user. |
| `DELETE` | `/api/menu-items/<id>/` | Yes | Delete a menu item created by the authenticated user. |
| `GET` | `/api/menu-categories/` | No | List categories with nested menu items. |

Full API request/response details are in:

```text
api_docs.md
```

## API Query Examples

Filter by category:

```text
/api/menu-items/?category=1
```

Filter by availability:

```text
/api/menu-items/?is_available=true
```

Search by name:

```text
/api/menu-items/?search=rice
```

Order by price:

```text
/api/menu-items/?ordering=price
```

Order by highest price first:

```text
/api/menu-items/?ordering=-price
```

## Postman Auth Notes

Single-token auth:

```text
POST /api/auth-token/
```

Body:

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

Use the returned token in Postman:

```text
Authorization: Token your-token
```

JWT auth:

```text
POST /api/token/
```

Body:

```json
{
  "username": "your-username",
  "password": "your-password"
}
```

Use the returned access token:

```text
Authorization: Bearer your-access-token
```

To refresh JWT access:

```text
POST /api/token/refresh/
```

Body:

```json
{
  "refresh": "your-refresh-token"
}
```

## Useful Commands

Run system checks:

```powershell
python manage.py check
```

Run all tests:

```powershell
python manage.py test
```

Create migrations:

```powershell
python manage.py makemigrations
```

Apply migrations:

```powershell
python manage.py migrate
```

Collect static files:

```powershell
python manage.py collectstatic --noinput
```

Update dependency list:

```powershell
pip freeze > requirements.txt
```

## Deployment Notes

The project includes:

- `Procfile` with the Gunicorn start command.
- `requirements.txt` with installed packages.
- WhiteNoise static-file serving.
- `STATIC_ROOT = staticfiles`.
- `DATABASE_URL` support through `dj-database-url`.

Before deploying:

- Set `DEBUG=False`.
- Set a strong `SECRET_KEY`.
- Set the real deployment domain in `ALLOWED_HOSTS`.
- Use a PostgreSQL `DATABASE_URL`.
- Run migrations.
- Run `collectstatic`.
- Restrict CORS for the deployed domain when ready.
- Configure real media-file hosting for uploaded menu item images.

## Verification Completed

The project has been checked with:

```powershell
python manage.py check
python manage.py test
python manage.py collectstatic --noinput
python -m waitress --listen=127.0.0.1:8080 happymeal.wsgi:application
```

Recent focused verification also confirmed the menu item add/edit flow still passes tests after styling changes.

## Final Summary

HappyMeal is now a full restaurant ordering system with customer ordering, staff management, image-backed menu items, secure authentication flows, API access, Postman documentation, deployment-ready settings, and a styled dark restaurant interface.

## CONCLUSION
This project demonstrates a comprehensive Django application with both website and API components, secure authentication, media handling, and deployment considerations. The added features and improvements provide a robust foundation for a real-world restaurant ordering system.