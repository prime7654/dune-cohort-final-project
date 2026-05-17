# HappyMeal Restaurant Ordering System

HappyMeal is a Django restaurant ordering system for browsing meals, managing menu content, placing customer orders, and tracking order status from a staff dashboard.

The project includes a public restaurant website, customer authentication, protected cart and checkout flows, menu/category management, customer order history, and staff-only administrative tools.

## Work Completed On May 17, 2026

The project was extended with a Django REST Framework API, Postman testing support, and restaurant-focused visual styling.

### API Work

- Added `rest_framework` to `INSTALLED_APPS`.
- Added `restaurants/serializers.py`.
- Added `MenuItemSerializer` with all menu item fields and nested `menu_category` data.
- Added `MenuCategorySerializer` with `menu_item_count` using `SerializerMethodField`.
- Added menu item API views inside `restaurants/views.py`.
- Added API routes inside `restaurants/urls.py`.
- Kept API naming aligned with the existing models: `MenuItem` and `MenuCategory`.

### API Endpoints Added

| Method | URL | Purpose |
| --- | --- | --- |
| `GET` | `/api/menu-items/` | List all menu items |
| `POST` | `/api/menu-items/` | Create a menu item |
| `GET` | `/api/menu-items/<id>/` | Retrieve one menu item |
| `PUT` | `/api/menu-items/<id>/` | Fully update one menu item |
| `DELETE` | `/api/menu-items/<id>/` | Delete one menu item |
| `GET` | `/api/menu-categories/` | List menu categories with menu item counts and nested menu items |

### API Testing Support

- Added `restaurants/test_api.py` with API tests for list, create, retrieve, update, delete, and category listing.
- Added `HappyMeal_API.postman_collection.json` for Postman endpoint testing.
- Confirmed the API endpoints work in Postman.

### Styling Work

- Updated the global website background from plain white to a dark restaurant-style background.
- Styled menu and category intro banners with a dark smoky gold image overlay.
- Styled the About page story panel and FAQ section with warm brown/gold cards.
- Updated button and text contrast so dark sections stay readable.
- Added a stylesheet cache version in `base.html` so browser styling updates load correctly.

### Verification

The following checks were run successfully:

```powershell
python manage.py check
python manage.py test restaurants.test_api
python manage.py test
```

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

### Menu And Cart Features

- Menu item CRUD with image upload.
- Category CRUD with item counts.
- Stock-aware cart.
- Out-of-stock items cannot be added to cart.
- Cart quantities are capped by available stock.
- Checkout reduces menu item stock after an order is placed.

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
|   |-- context_processors.py
|   |-- forms.py
|   |-- models.py
|   |-- serializers.py
|   |-- test_api.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   |-- static/
|   |   `-- restaurants/css/style.css
|   `-- templates/
|       |-- base.html
|       |-- registration/
|       `-- restaurants/
|-- orders/
|   |-- admin.py
|   |-- forms.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/orders/
|-- media/
|   `-- menu_items/
|-- HappyMeal_API.postman_collection.json
|-- db.sqlite3
|-- manage.py
`-- README.md
```

## Main Apps

### `restaurants`

Handles the public website, menu items, categories, cart session behavior, registration, dashboard, and shared templates.

Main models:

- `MenuCategory`
- `MenuItem`

### `orders`

Handles checkout, customer profiles, order records, order items, order history, and staff order status updates.

Main models:

- `Customer`
- `Order`
- `OrderItem`

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

### API

| URL | Purpose |
| --- | --- |
| `/api/menu-items/` | List menu items with nested menu category data, or create a menu item |
| `/api/menu-items/<id>/` | Retrieve, fully update, or delete one menu item |
| `/api/menu-categories/` | List menu categories with `menu_item_count` and nested menu items |

Postman collection:

```text
HappyMeal_API.postman_collection.json
```

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
pip install django djangorestframework Pillow
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
- Customers can only view their own orders.
- Staff users can manage menu/category content.
- Staff users can view the dashboard and update order statuses.
- Delete actions use confirmation pages and require `POST`.
- Forms include CSRF protection.
- Password reset uses Django's email reset flow with console email backend in development.

## Testing

The project includes tests for:

- Public page rendering
- Authentication and registration
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
This project demonstrates a full-stack Django restaurant ordering system with a public website, customer authentication, cart and checkout flows, staff dashboard, and a REST API. The code is organized into two main apps (`restaurants` and `orders`) with clear separation of concerns. The project includes comprehensive features for customers and staff, as well as testing support to ensure functionality. The API allows for future expansion, such as mobile app integration or third-party services. The styling provides a warm restaurant atmosphere, and the project structure allows for easy maintenance and scalability.
