# Dune Cohort Final Project

This workspace contains the HappyMeal restaurant ordering system in the `restaurant-ordering-system/` folder.

## Project Summary

HappyMeal is a Django-based restaurant ordering system. The previous project already included:

- Public menu browsing
- Customer registration, login, logout, and password reset
- Login-protected cart and checkout
- Customer order history
- Staff-only dashboard
- Staff order status management
- Staff-only menu and category CRUD
- Stock-aware cart and menu availability
- Image uploads for menu items

## Latest Work Completed

On May 17, 2026, the project was improved with:

- Django REST Framework API support.
- `MenuItemSerializer` and `MenuCategorySerializer`.
- API endpoints for menu items and menu categories.
- Nested menu category data on menu item responses.
- `menu_item_count` on menu category responses.
- API tests in `restaurants/test_api.py`.
- A Postman collection: `restaurant-ordering-system/HappyMeal_API.postman_collection.json`.
- Dark restaurant-style background design.
- Dark smoky gold menu/category banners.
- Warm brown/gold About page panels and FAQ cards.
- README updates for setup, API routes, and testing.

## Main Project Folder

```text
restaurant-ordering-system/
```

See the full setup guide, routes, features, roles, and testing instructions in:

```text
restaurant-ordering-system/README.md
```

## Main API Routes

| Method | URL | Purpose |
| --- | --- | --- |
| `GET` | `/api/menu-items/` | List menu items |
| `POST` | `/api/menu-items/` | Create a menu item |
| `GET` | `/api/menu-items/<id>/` | Retrieve one menu item |
| `PUT` | `/api/menu-items/<id>/` | Fully update one menu item |
| `DELETE` | `/api/menu-items/<id>/` | Delete one menu item |
| `GET` | `/api/menu-categories/` | List categories with menu items |

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

## Verification

The project was checked with:

```powershell
python manage.py check
python manage.py test
```
## Conclusion
This project demonstrates a comprehensive Django application with both website and API components, secure authentication, media handling, and deployment considerations. The added features and improvements provide a robust foundation for a real-world restaurant ordering system.