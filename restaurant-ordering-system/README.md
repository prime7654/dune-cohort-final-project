# HappyMeal Restaurant Ordering System

HappyMeal is a Django restaurant ordering project that lets customers browse a styled food menu, view dish details, explore menu categories, and add available meals to a session-based cart.

The project uses Django with SQLite for local development, Bootstrap CDN for layout support, and custom CSS for a warmer restaurant-style interface.

## Features

- Polished restaurant homepage with a visual hero section
- Styled navigation bar with Home, Menu, About, and Cart links
- Database-backed menu list
- Menu detail pages for individual food items
- Category list with menu item counts
- In Stock and Out of Stock badges using `is_available`
- Session-based cart
- Add to Cart buttons on menu cards
- Quantity selector on food detail pages
- Cart page with item summary, quantity update, remove button, and subtotal
- Custom styled 404 page
- Seeded restaurant categories and food items through migrations
- Matching food image URLs for menu items
- Django admin support for managing records
- Automated tests for pages and cart behavior

## Tech Stack

- Python
- Django
- SQLite
- Django Templates
- Bootstrap CDN
- Custom inline CSS

## Main Apps

### `restaurants`

Handles the public restaurant website:

- Homepage
- Menu list
- Menu item detail pages
- Category list
- Cart pages and cart actions
- Shared templates and styling
- Seed menu data migrations

### `orders`

Stores order-related models:

- Customers
- Orders
- Order items

The cart currently works as a customer-facing ordering preview. A full checkout form can be connected later to create real `Order` and `OrderItem` records from the cart.

## Models

### `MenuCategory`

Located in `restaurants/models.py`.

| Field | Description |
| --- | --- |
| `name` | Category name such as Rice, Drinks, Starters, or Grills |
| `description` | Optional category description |

### `MenuItem`

Located in `restaurants/models.py`.

| Field | Description |
| --- | --- |
| `category` | Connects the item to a menu category |
| `name` | Food or drink name |
| `description` | Menu item description |
| `price` | Item price |
| `is_available` | Controls In Stock or Out of Stock display |
| `image_url` | Image URL displayed on menu cards and detail pages |
| `created_at` | Timestamp for when the item was created |

### `Customer`

Located in `orders/models.py`.

Stores customer contact and address details.

### `Order`

Located in `orders/models.py`.

Stores a customer's order, status, delivery address, notes, timestamps, and total price calculation.

### `OrderItem`

Located in `orders/models.py`.

Stores one menu item inside an order, including quantity, saved unit price, and line total.

## Seeded Menu Data

The project includes seed data through Django migrations.

Current seeded categories:

- Starters
- Main Meals
- Grills
- Drinks

Current seeded menu items:

- Pepper Soup
- Spring Rolls
- Fried Rice and Chicken
- Pounded Yam and Egusi
- Suya Platter
- Grilled Fish
- Chapman
- Zobo Drink

The menu also supports any additional items added through the Django admin or Django shell.

## Pages And Routes

| URL | View | Description |
| --- | --- | --- |
| `/` | `home` | Restaurant homepage |
| `/menu_list/` | `menu_list` | Full menu list |
| `/menu/<id>/` | `menu_detail` | Detail page for one menu item |
| `/categories/` | `category_list` | Menu categories and item counts |
| `/cart/` | `cart_detail` | Customer cart |
| `/cart/add/<id>/` | `cart_add` | Adds an available item to the cart |
| `/cart/update/<id>/` | `cart_update` | Updates item quantity in the cart |
| `/cart/remove/<id>/` | `cart_remove` | Removes item from the cart |
| `/about/` | `about` | Restaurant about page |
| `/admin/` | Django admin | Admin dashboard |

## Cart Behavior

The cart uses Django sessions, so each browser session has its own cart.

Customers can:

- Add food from the menu page
- Add food from the detail page with quantity
- View cart count in the navbar
- Update item quantity
- Remove items
- See cart subtotal

Unavailable items cannot be added to the cart.

## Templates

Templates are located in `restaurants/templates/`.

```text
restaurants/templates/
|-- base.html
`-- restaurants/
    |-- 404.html
    |-- about.html
    |-- cart_detail.html
    |-- category_list.html
    |-- home.html
    |-- menu_detail.html
    `-- menu_list.html
```

All public pages extend `base.html`.

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
|   |-- apps.py
|   |-- context_processors.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/
|-- orders/
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- tests.py
|   |-- views.py
|   `-- migrations/
|-- manage.py
`-- README.md
```

## Setup Instructions

### 1. Open the project folder

```powershell
cd C:\Users\ogbon\OneDrive\Desktop\dune-cohort-final-project\restaurant-ordering-system
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

If `python` does not work, use:

```powershell
py -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

### 4. Install Django

```powershell
pip install django
```

### 5. Apply migrations

```powershell
python manage.py migrate
```

This creates the database tables and loads the seeded menu categories, food items, and menu images.

### 6. Create an admin user

```powershell
python manage.py createsuperuser
```

### 7. Run the development server

```powershell
python manage.py runserver
```

Open the site:

```text
http://127.0.0.1:8000/
```

## Useful Development Commands

Run all tests:

```powershell
python manage.py test
```

Check migrations:

```powershell
python manage.py showmigrations
```

Create new migrations after model changes:

```powershell
python manage.py makemigrations
```

Apply migrations:

```powershell
python manage.py migrate
```

## Migration Status

Current restaurant migrations:

```text
[X] 0001_initial
[X] 0002_seed_menu_data
[X] 0003_add_menu_images
[X] 0004_replace_with_matching_menu_images
[X] 0005_use_crispy_spring_roll_image
```

Current order migrations:

```text
[X] 0001_initial
```

## Testing

The test suite currently covers:

- Menu list rendering
- Menu detail rendering
- Category count rendering
- Home page rendering
- About page rendering
- Custom 404 page rendering
- Empty cart page
- Adding items to cart
- Updating cart quantity
- Removing cart items
- Blocking unavailable items from cart

Latest verified result:

```text
Ran 12 tests
OK
```

## Notes

- The cart is session-based and does not yet create database orders.
- A future checkout page can connect cart contents to the existing `Customer`, `Order`, and `OrderItem` models.
- Menu images are loaded from external URLs, so internet access may affect image display.
- Food records can be managed from the Django admin after creating a superuser.

## CONCLUSION

HappyMeal Restaurant Ordering System is a polished Django web application for browsing restaurant meals, viewing food details, exploring menu categories, and adding available items to a cart. The project now combines database-backed models, Django templates, Bootstrap styling, seeded menu data, food images, and a session-based cart to create a smooth customer-facing restaurant experience.

The system organizes menu categories, menu items, customers, orders, and order items in a clear structure. Customers can view available meals, see prices and stock status, add items to their cart, update quantities, and remove items before ordering. The project is also tested with Django unit tests to confirm that the main pages and cart features work correctly.

Overall, the project demonstrates a strong foundation for a restaurant ordering platform. A future improvement would be connecting the cart to a full checkout form so customer orders can be saved directly into the existing order models.