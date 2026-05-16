# Dune Cohort Final Project

This workspace contains the HappyMeal restaurant ordering system in the `restaurant-ordering-system/` folder.

## Project Summary

HappyMeal is a Django-based restaurant ordering system with:

- Public menu browsing
- Customer registration, login, logout, and password reset
- Login-protected cart and checkout
- Customer order history
- Staff-only dashboard
- Staff order status management
- Staff-only menu and category CRUD
- Stock-aware cart and menu availability
- Image uploads for menu items

## Main Project Folder

```text
restaurant-ordering-system/
```

See the full setup guide, routes, features, roles, and testing instructions in:

```text
restaurant-ordering-system/README.md
```

## Quick Start

```powershell
cd restaurant-ordering-system
.\venv\Scripts\activate
python manage.py migrate
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```
