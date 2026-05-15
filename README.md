# Dune Cohort Final Project

This workspace contains the completed restaurant ordering system project in the `restaurant-ordering-system/` folder.

## Previous Project Work

The restaurant website was upgraded into a fuller Django menu management system. The work completed includes:

- Full CRUD for menu items and categories.
- Restaurant-friendly routes such as `/menu-items/` and `/categories/`.
- Validated create and edit forms with CSRF protection.
- Delete confirmation pages that delete only on `POST`.
- Success flash messages after create, update, and delete actions.
- Menu item stock tracking and stock-aware cart behavior.
- `ImageField` support for uploaded menu item images.
- Local media setup with `MEDIA_URL` and `MEDIA_ROOT`.
- Seeded menu images moved into `media/menu_items/`.
- Customized Django admin with search, filters, stock display, and a `Mark as out of stock` action.
- A custom CSS file for restaurant-style menu, category, and footer styling.
- Tests covering CRUD, cart behavior, images, and admin action behavior.

See `restaurant-ordering-system/README.md` for setup instructions, routes, and full project details.
