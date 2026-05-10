# HappyMeal Restaurant Ordering System

HappyMeal Restaurant is a simple Django web project for managing a restaurant menu and customer orders. The project started with basic pages for the homepage, menu list, about page, and a custom 404 page. It now includes database models that allow the restaurant to store menu categories, menu items, customers, orders, and the individual items inside each order.

The project is built with Django and uses SQLite for local development.

## Project Description

HappyMeal Restaurant helps organize the main parts of a restaurant ordering workflow:

- Restaurant staff can create food categories such as rice, burgers, drinks, and desserts.
- Restaurant staff can add menu items with prices and availability.
- Customers can be recorded with contact and address details.
- Orders can be created for customers.
- Each order can contain one or more menu items with quantities and saved prices.

## Models

### MenuCategory

Located in `restaurants/models.py`.

This model groups menu items into categories.

| Field | Type | Description |
| --- | --- | --- |
| `name` | `CharField` | Category name, for example `Rice` or `Drinks`. Must be unique. |
| `description` | `TextField` | Optional description of the category. |

Extra behavior:

- Categories are ordered by `name`.
- The plural name in Django admin is shown as `menu categories`.

### MenuItem

Located in `restaurants/models.py`.

This model represents a food or drink item that can be ordered.

| Field | Type | Description |
| --- | --- | --- |
| `category` | `ForeignKey` | Connects the item to a `MenuCategory`. |
| `name` | `CharField` | Name of the menu item. |
| `description` | `TextField` | Optional item description. |
| `price` | `DecimalField` | Price of the menu item. |
| `is_available` | `BooleanField` | Shows whether the item is currently available. |
| `image_url` | `URLField` | Optional image URL for the item. |
| `created_at` | `DateTimeField` | Automatically stores when the item was created. |

Extra behavior:

- Menu items are ordered by category name, then item name.
- The same item name cannot be repeated inside the same category.

### Customer

Located in `orders/models.py`.

This model stores customer information.

| Field | Type | Description |
| --- | --- | --- |
| `full_name` | `CharField` | Customer's full name. |
| `phone_number` | `CharField` | Customer's phone number. |
| `email` | `EmailField` | Optional customer email address. |
| `address` | `TextField` | Optional customer address. |
| `created_at` | `DateTimeField` | Automatically stores when the customer record was created. |

Extra behavior:

- Customers are ordered by `full_name`.

### Order

Located in `orders/models.py`.

This model represents a customer's full order.

| Field | Type | Description |
| --- | --- | --- |
| `customer` | `ForeignKey` | Connects the order to a `Customer`. |
| `status` | `CharField` | Tracks the order state. |
| `delivery_address` | `TextField` | Optional delivery address for the order. |
| `notes` | `TextField` | Optional order notes. |
| `created_at` | `DateTimeField` | Automatically stores when the order was created. |
| `updated_at` | `DateTimeField` | Automatically updates whenever the order changes. |

Available order statuses:

- `pending`
- `confirmed`
- `preparing`
- `ready`
- `delivered`
- `cancelled`

Extra behavior:

- Orders are ordered from newest to oldest.
- The `total_price` property adds up all related order items.
- The customer relationship uses `PROTECT`, so old orders are not accidentally broken if someone tries to delete a customer.

### OrderItem

Located in `orders/models.py`.

This model represents one menu item inside an order.

| Field | Type | Description |
| --- | --- | --- |
| `order` | `ForeignKey` | Connects the item to an `Order`. |
| `menu_item` | `ForeignKey` | Connects the order item to a `MenuItem`. |
| `quantity` | `PositiveIntegerField` | Number of this menu item ordered. |
| `unit_price` | `DecimalField` | Price of the menu item at the time of ordering. |

Extra behavior:

- The `line_total` property multiplies `quantity` by `unit_price`.
- If `unit_price` is empty when saving, it is automatically copied from the selected menu item's current price.
- The menu item relationship uses `PROTECT`, so menu items used in past orders cannot be deleted accidentally.

## Features Implemented

- Created restaurant menu models:
  - `MenuCategory`
  - `MenuItem`
- Created order management models:
  - `Customer`
  - `Order`
  - `OrderItem`
- Added model relationships using Django foreign keys.
- Added order status choices using `models.TextChoices`.
- Added automatic timestamps with `auto_now_add` and `auto_now`.
- Added price calculations with `total_price` and `line_total`.
- Registered all models in the Django admin.
- Added admin list displays, filters, and search fields.
- Created and applied initial migrations for the `restaurants` and `orders` apps.

## ORM Operations Performed

The following examples can be run inside the Django shell.

Start the shell:

```powershell
.\venv\Scripts\python.exe manage.py shell
```

Import the models:

```python
from decimal import Decimal
from restaurants.models import MenuCategory, MenuItem
from orders.models import Customer, Order, OrderItem
```

### Create Records

Create a menu category:

```python
rice = MenuCategory.objects.create(
    name="Rice",
    description="Rice-based meals"
)
```

Create a menu item:

```python
jollof = MenuItem.objects.create(
    category=rice,
    name="Jollof Rice",
    description="Party-style jollof rice",
    price=Decimal("2500.00"),
    is_available=True
)
```

Create a customer:

```python
customer = Customer.objects.create(
    full_name="Ada Okafor",
    phone_number="08012345678",
    address="Lagos"
)
```

Create an order:

```python
order = Order.objects.create(
    customer=customer,
    delivery_address=customer.address
)
```

Add an item to the order:

```python
OrderItem.objects.create(
    order=order,
    menu_item=jollof,
    quantity=2
)
```

### Read Records

Get all menu items:

```python
MenuItem.objects.all()
```

Get only available menu items:

```python
MenuItem.objects.filter(is_available=True)
```

Get one menu item by name:

```python
MenuItem.objects.get(name="Jollof Rice")
```

Get pending orders:

```python
Order.objects.filter(status=Order.Status.PENDING)
```

Search for a customer:

```python
Customer.objects.filter(full_name__icontains="ada")
```

Calculate an order total:

```python
order.total_price
```

### Update Records

Update a menu item price:

```python
jollof.price = Decimal("3000.00")
jollof.save()
```

Mark a menu item as unavailable:

```python
MenuItem.objects.filter(name="Jollof Rice").update(is_available=False)
```

Update an order status:

```python
order.status = Order.Status.PREPARING
order.save()
```

### Delete Records

Delete unused records:

```python
MenuItem.objects.filter(name="Unused Item").delete()
```

Menu items that have already been used in an order are protected. If a menu item is linked to an `OrderItem`, Django raises a `ProtectedError` instead of deleting it.

For real restaurant data, the safer option is to mark the item unavailable:

```python
MenuItem.objects.filter(name="Jollof Rice").update(is_available=False)
```

For testing only, related order items can be deleted first:

```python
OrderItem.objects.filter(menu_item__name="Jollof Rice").delete()
MenuItem.objects.filter(name="Jollof Rice").delete()
```

## Setup Instructions

### 1. Open the Project Folder

```powershell
cd C:\Users\ogbon\OneDrive\Desktop\dune-cohort-final-project\restaurant-ordering-system
```

### 2. Create a Virtual Environment

If the `venv` folder does not already exist, create it:

```powershell
python -m venv venv
```

If `python` does not work on your machine, try:

```powershell
py -m venv venv
```

### 3. Activate the Virtual Environment

```powershell
.\venv\Scripts\activate
```

### 4. Install Django

```powershell
pip install django
```

### 5. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

### 7. Run the Development Server

```powershell
python manage.py runserver
```

### 8. Open the Project

Main pages:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/menu_list/
http://127.0.0.1:8000/about/
```

Django admin:

```text
http://127.0.0.1:8000/admin/
```

## Available Routes

| URL Path | View Function | Description |
| --- | --- | --- |
| `/` | `home()` | Displays the HappyMeal welcome message. |
| `/menu_list/` | `menu_list()` | Displays a basic menu list message. |
| `/about/` | `about()` | Displays information about HappyMeal Restaurant. |
| `/admin/` | Django admin | Opens the Django admin dashboard. |

## Migration Status

The following project migrations have been created and applied:

```text
restaurants
 [X] 0001_initial

orders
 [X] 0001_initial
```

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
|   |-- models.py
|   |-- views.py
|   `-- migrations/
|       `-- 0001_initial.py
|-- orders/
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- views.py
|   `-- migrations/
|       `-- 0001_initial.py
|-- screenshots/
|-- manage.py
`-- README.md
```

## Current Status

The project now has a working Django structure, basic restaurant pages, database-backed models, Django admin registration, and applied migrations. The next improvement would be connecting the menu and order models to templates and forms so users can place orders through the browser.
