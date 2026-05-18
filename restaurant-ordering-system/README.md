# HappyMeal Restaurant Ordering System

HappyMeal is a Django restaurant ordering system for browsing meals, managing menu content, placing customer orders, and tracking order status from a staff dashboard.

The project includes a public restaurant website, customer authentication, protected cart and checkout flows, menu/category management, customer order history, staff-only administrative tools, and a Django REST Framework API.

## Features

### Customer Features

- Browse the restaurant menu and categories.
- View menu item details, stock status, prices, and images.
- Register, login, logout, and reset passwords.
- Add items to cart only after logging in.
- Checkout with delivery address, phone number, email, and notes.
- View personal order history from `My Orders`.
- View order details and order status.

### Staff/Admin Features

- Staff-only dashboard at `/dashboard/`.
- Dashboard separates customers, admins, and superusers.
- Dashboard shows menu counts, active orders, delivered orders, and recent orders.
- Staff can update order status directly from the dashboard.
- Staff-only menu item and category create, edit, and delete views.
- Django admin support for menu items, categories, customers, orders, and order items.

### API Features

- JWT authentication at `/api/token/` and `/api/token/refresh/`.
- Single-token authentication at `/api/auth-token/`.
- Authenticated-only menu item create, update, and delete.
- Creator-only menu item update and delete.
- Paginated menu item listing with 6 items per page.
- Filtering by category and availability.
- Search by menu item name.
- Ordering by price.
- CORS headers enabled for development/testing.
- API details documented in `api_docs.md`.

## User Roles

| Role | Access |
| --- | --- |
| Guest | Can browse public pages and menu. Cannot add to cart or place orders. |
| Customer | Can add to cart, checkout, and view their own orders. |
| Staff/Admin | Can manage menu/category content, view dashboard, and update orders. |
| Superuser | Has staff access plus Django admin superuser permissions. |

## Tech Stack

- Python
- Django
- SQLite
- Django REST Framework
- DRF token authentication
- Simple JWT
- django-filter
- django-cors-headers
- Django Templates
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
|   |-- admin.py
|   |-- auth_rate_limit.py
|   |-- auth_views.py
|   |-- context_processors.py
|   |-- forms.py
|   |-- models.py
|   |-- pagination.py
|   |-- permissions.py
|   |-- serializers.py
|   |-- test_api.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   |-- static/
|   `-- templates/
|-- orders/
|-- media/
|-- api_docs.md
|-- HappyMeal_API.postman_collection.json
|-- db.sqlite3
|-- manage.py
`-- README.md
```

## Important Routes

### Public Pages

| URL | Purpose |
| --- | --- |
| `/` | Home page |
| `/about/` | About and FAQ page |
| `/menu_list/` | Menu listing |
| `/menu/<id>/` | Public menu item detail |
| `/categories/` | Category listing |
| `/categories/<id>/` | Category detail |

### Authentication

| URL | Purpose |
| --- | --- |
| `/accounts/register/` | Customer registration |
| `/accounts/login/` | Login |
| `/accounts/logout/` | Logout |
| `/accounts/password-reset/` | Password reset request |
| `/accounts/reset/<uidb64>/<token>/` | Password reset confirmation |

### API

| URL | Purpose |
| --- | --- |
| `/api/auth-token/` | Get a single API auth token |
| `/api/token/` | Get JWT access and refresh tokens |
| `/api/token/refresh/` | Refresh a JWT access token |
| `/api/menu-items/` | List paginated menu items with filtering, search, ordering, or create a menu item |
| `/api/menu-items/<id>/` | Retrieve, fully update, or delete one creator-owned menu item |
| `/api/menu-categories/` | List menu categories with `menu_item_count` and nested menu items |

### Cart And Orders

| URL | Purpose |
| --- | --- |
| `/cart/` | Customer cart, login required |
| `/cart/add/<id>/` | Add item to cart, login required |
| `/cart/update/<id>/` | Update cart quantity, login required |
| `/cart/remove/<id>/` | Remove item from cart, login required |
| `/checkout/` | Place an order, login required |
| `/orders/` | Customer order history |
| `/orders/<id>/` | Order detail |

### Staff/Admin

| URL | Purpose |
| --- | --- |
| `/dashboard/` | Staff dashboard |
| `/dashboard/orders/<id>/status/` | Update order status |
| `/menu-items/add/` | Add menu item |
| `/menu-items/<id>/edit/` | Edit menu item |
| `/menu-items/<id>/delete/` | Delete menu item |
| `/categories/add/` | Add category |
| `/categories/<id>/edit/` | Edit category |
| `/categories/<id>/delete/` | Delete category |
| `/admin/` | Django admin |

## Setup

### 1. Open the project folder

```powershell
cd C:\Users\ogbon\OneDrive\Desktop\dune-cohort-final-project\restaurant-ordering-system
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\activate
```

If `python` is not available, try:

```powershell
py -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install django djangorestframework djangorestframework-simplejwt django-filter django-cors-headers Pillow
```

### 4. Apply migrations

```powershell
python manage.py migrate
```

### 5. Create a superuser

```powershell
python manage.py createsuperuser
```

### 6. Run the development server

```powershell
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Useful Commands

Run tests:

```powershell
python manage.py test
```

Run Django system checks:

```powershell
python manage.py check
```

Create migrations:

```powershell
python manage.py makemigrations
```

Apply migrations:

```powershell
python manage.py migrate
```

## Security And Permissions

- Guests can browse, but cannot add to cart or checkout.
- Customers must login before ordering.
- Login and token endpoints pause further attempts for 5 minutes after 5 failed password attempts.
- Customers can only view their own orders.
- Staff users can manage menu/category content.
- Staff users can view the dashboard and update order statuses.
- Delete actions use confirmation pages and require `POST`.
- Forms include CSRF protection.
- Password reset uses Django's email reset flow with console email backend in development.

## Testing

The project includes tests for:

- Public page rendering
- Authentication, registration, and sign-in cooldown
- Single-token and JWT API authentication
- Password reset email flow
- Staff dashboard access
- Menu item CRUD
- Category CRUD
- Cart login protection and stock behavior
- Checkout and order creation
- Customer order history
- Staff order status updates

Current verified test command:

```powershell
python manage.py test
```

## Notes

- Uploaded menu item images are stored in `media/menu_items/`.
- During development, media files are served through Django when `DEBUG = True`.
- Password reset emails print to the console by default because the project uses Django's console email backend.
- Before deployment, move `SECRET_KEY` to an environment variable, set `DEBUG = False`, and configure `ALLOWED_HOSTS`.
 
## CONCLUSION
This project demonstrates a full-stack Django restaurant ordering system with public browsing, customer authentication, cart and checkout flows, staff dashboard, and a REST API. It includes security measures, permissions, and comprehensive testing to ensure a robust application.