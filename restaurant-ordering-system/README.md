# ToriloShop Restaurant Ordering System

ToriloShop is a Django-based restaurant ordering system that allows users to browse menu items, view categories, and manage menu data through full Create, Read, Update, and Delete operations.

The project now supports complete CRUD for:

- Menu items, represented by the `MenuItem` model
- Categories, represented by the `MenuCategory` model

Users can create new menu items and categories, view existing records, edit saved records through pre-filled forms, and delete records only after confirming the action.

Menu items also support stock tracking and image uploads. Uploaded images are served from the local `media/` directory during development and are displayed as thumbnails on list pages and larger images on detail pages.

## Project Description

ToriloShop now includes full menu item and category management for a restaurant menu.

Menu item CRUD allows the system to:

- Create a new menu item from `/menu-items/add/`
- Read menu items from `/menu-items/` and individual menu item details from `/menu-items/<id>/`
- Update an existing menu item from `/menu-items/<id>/edit/`
- Delete a menu item from `/menu-items/<id>/delete/` after confirmation

Category CRUD allows the system to:

- Create a new category from `/categories/add/`
- Read categories from `/categories/` and individual category details from `/categories/<id>/`
- Update an existing category from `/categories/<id>/edit/`
- Delete a category from `/categories/<id>/delete/` after confirmation

All create, edit, and delete actions show success flash messages after completion. Delete actions are protected so records are removed only when the confirmation form is submitted with `POST`.

## Features Implemented

### Menu Item Features

| Feature | URL | Description |
| --- | --- | --- |
| Menu Item List | `/menu-items/` | Displays all menu items. |
| Menu Item Detail | `/menu-items/<id>/` | Displays the full details for one menu item. |
| Add Menu Item Form | `/menu-items/add/` | Creates a new menu item with category, name, description, price, stock, availability, and uploaded image fields. |
| Edit Menu Item Form | `/menu-items/<id>/edit/` | Shows a pre-filled form for an existing menu item and saves updated values, including stock and image changes. |
| Delete Menu Item Confirmation | `/menu-items/<id>/delete/` | Shows a confirmation page. The menu item is deleted only after submitting the POST form. |

### Image And Stock Features

| Feature | Description |
| --- | --- |
| Menu item image upload | Uses Django `ImageField` to upload images into `media/menu_items/`. |
| List page thumbnail | Shows a thumbnail image for each menu item on the menu list page. |
| Detail page image | Shows a larger image for the selected menu item on the detail page. |
| Seeded local images | The original menu image URLs were downloaded into `media/menu_items/` and are now used through `ImageField`. |
| Stock field | Tracks how many units are available for each menu item. |
| Stock-aware cart | Prevents out-of-stock menu items from being added and caps cart quantities by available stock. |

### Category Features

| Feature | URL | Description |
| --- | --- | --- |
| Category List | `/categories/` | Displays all categories and their menu item counts. |
| Category Detail | `/categories/<id>/` | Displays one category and the menu items inside it. |
| Add Category Form | `/categories/add/` | Creates a new category with name and description fields. |
| Edit Category Form | `/categories/<id>/edit/` | Shows a pre-filled form for an existing category and saves updated values. |
| Delete Category Confirmation | `/categories/<id>/delete/` | Shows a confirmation page. The category is deleted only after submitting the POST form. |

### Styling Features

- Custom restaurant-style CSS is loaded from `restaurants/static/restaurants/css/style.css`.
- The menu page uses image-led cards, category chips, stock badges, and polished ordering actions.
- The categories page uses styled restaurant section cards with item counts and clear management actions.
- The footer includes brand details, quick links, visit information, opening hours, and a cart link.

## Validation And Security

- All forms use Django `ModelForm` validation.
- Required fields are validated before saving.
- Menu item price must be at least `0.01`.
- Available menu items must have stock above `0`.
- Duplicate menu item names are blocked within the same category.
- Category names must be unique.
- Every create, edit, and delete form includes `{% csrf_token %}`.
- Delete pages use confirmation forms and only delete records on `POST`.
- Success messages are displayed after create, update, and delete actions.

## Tech Stack

- Python
- Django
- SQLite
- Django Templates
- Bootstrap
- Pillow

## Admin Features

The Django admin includes custom menu item management:

- `list_display` shows name, price, category, stock, and availability.
- `search_fields` supports searching by menu item name and category name.
- `list_filter` supports filtering by category and availability.
- A custom admin action, `Mark as out of stock`, sets `stock=0` and `is_available=False`.

## Project Structure

```text
restaurant-ordering-system/
|-- happymeal/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
|-- restaurants/
|   |-- forms.py
|   |-- models.py
|   |-- urls.py
|   |-- views.py
|   |-- tests.py
|   |-- migrations/
|   |-- static/
|   |   `-- restaurants/
|   |       `-- css/
|   |           `-- style.css
|   `-- templates/
|       |-- base.html
|       `-- restaurants/
|           |-- category_detail.html
|           |-- category_form.html
|           |-- category_list.html
|           |-- confirm_delete.html
|           |-- menu_detail.html
|           |-- menu_list.html
|           `-- menu_item_form.html
|-- orders/
|-- db.sqlite3
|-- media/
|-- manage.py
`-- README.md
```

## Setup Instructions

Follow these steps to run the project locally.

### 1. Open the project folder

```powershell
cd C:\Users\ogbon\OneDrive\Desktop\dune-cohort-final-project\restaurant-ordering-system
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

If `python` does not work on your machine, try:

```powershell
py -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

### 4. Install dependencies

```powershell
pip install django Pillow
```

### 5. Apply database migrations

```powershell
python manage.py migrate
```

### 6. Run the development server

```powershell
python manage.py runserver
```

Open the project in your browser:

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

Create a superuser for the admin dashboard:

```powershell
python manage.py createsuperuser
```

Open the admin dashboard:

```text
http://127.0.0.1:8000/admin/
```

## Main Routes

| URL | Purpose |
| --- | --- |
| `/` | Home page |
| `/menu_list/` | Public menu list |
| `/menu/<id>/` | Public menu item detail page |
| `/menu-items/` | Menu item list |
| `/menu-items/add/` | Add menu item |
| `/menu-items/<id>/` | Menu item detail |
| `/menu-items/<id>/edit/` | Edit menu item |
| `/menu-items/<id>/delete/` | Delete menu item confirmation |
| `/categories/` | Category list |
| `/categories/add/` | Add category |
| `/categories/<id>/` | Category detail |
| `/categories/<id>/edit/` | Edit category |
| `/categories/<id>/delete/` | Delete category confirmation |
| `/cart/` | Cart page |

## Summary

ToriloShop now has a complete CRUD workflow for managing menu items and categories. The implementation includes validated forms, stock tracking, uploaded menu item images, custom restaurant styling, a polished menu page, styled category cards, an upgraded footer, media serving during development, admin search/filter/action support, pre-filled edit pages, safe delete confirmation pages, CSRF protection, success flash messages, and automated tests for the main behavior.
