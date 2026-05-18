# HappyMeal API Documentation

Base URL for local development: `http://127.0.0.1:8000`

For single-token authentication, use:

```http
Authorization: Token <auth_token>
```

For JWT authentication, use:

```http
Authorization: Bearer <access_token>
```

## Authentication

After 5 failed password attempts from the same username or IP address, the login/token endpoints return `429 Too Many Requests` for 5 minutes.

### Get Single Auth Token

- Method: `POST`
- URL: `/api/auth-token/`
- Auth required: No
- Request body:

```json
{
  "username": "chef",
  "password": "StrongPass123!"
}
```

- Success response: `200 OK`

```json
{
  "token": "single-auth-token"
}
```

- Postman authorization header:

```http
Authorization: Token single-auth-token
```

- Error responses:
  - `400 Bad Request` for invalid credentials before the cooldown limit is reached
  - `429 Too Many Requests` after too many failed password attempts

### Get JWT Tokens

- Method: `POST`
- URL: `/api/token/`
- Auth required: No
- Request body:

```json
{
  "username": "chef",
  "password": "StrongPass123!"
}
```

- Success response: `200 OK`

```json
{
  "refresh": "refresh-token",
  "access": "access-token"
}
```

- Postman authorization header:

```http
Authorization: Bearer access-token
```

- Error responses:
  - `401 Unauthorized` for invalid credentials before the cooldown limit is reached
  - `429 Too Many Requests` after too many failed password attempts

### Refresh JWT Access Token

- Method: `POST`
- URL: `/api/token/refresh/`
- Auth required: No
- Request body:

```json
{
  "refresh": "refresh-token"
}
```

- Success response: `200 OK`

```json
{
  "access": "new-access-token"
}
```

## Menu Items

### List Menu Items

- Method: `GET`
- URL: `/api/menu-items/`
- Auth required: No
- Query parameters:
  - `page`: page number
  - `category`: menu category ID
  - `is_available`: `true` or `false`
  - `search`: search menu item names
  - `ordering`: `price` or `-price`
- Success response: `200 OK`

```json
{
  "count": 12,
  "next": "http://127.0.0.1:8000/api/menu-items/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "menu_category": {
        "id": 1,
        "name": "Rice",
        "description": "Rice meals"
      },
      "created_by": {
        "id": 2,
        "username": "chef"
      },
      "name": "Jollof Rice",
      "description": "Party-style jollof rice",
      "price": "2500.00",
      "stock": 12,
      "is_available": true,
      "image": null,
      "created_at": "2026-05-18T09:00:00Z"
    }
  ]
}
```

### Create Menu Item

- Method: `POST`
- URL: `/api/menu-items/`
- Auth required: Yes
- Request body:

```json
{
  "menu_category_id": 1,
  "name": "Fried Rice",
  "description": "Vegetable fried rice",
  "price": "2800.00",
  "stock": 7,
  "is_available": true
}
```

- Success response: `201 Created`
- Notes:
  - `created_by` is set from the authenticated user.
  - Unauthenticated requests return `401 Unauthorized`.

### Get Menu Item Detail

- Method: `GET`
- URL: `/api/menu-items/<id>/`
- Auth required: No
- Success response: `200 OK`

```json
{
  "id": 1,
  "menu_category": {
    "id": 1,
    "name": "Rice",
    "description": "Rice meals"
  },
  "created_by": {
    "id": 2,
    "username": "chef"
  },
  "name": "Jollof Rice",
  "description": "Party-style jollof rice",
  "price": "2500.00",
  "stock": 12,
  "is_available": true,
  "image": null,
  "created_at": "2026-05-18T09:00:00Z"
}
```

### Update Menu Item

- Method: `PUT`
- URL: `/api/menu-items/<id>/`
- Auth required: Yes, and the authenticated user must be the creator
- Request body:

```json
{
  "menu_category_id": 1,
  "name": "Jollof Rice Deluxe",
  "description": "Updated party-style jollof rice",
  "price": "3000.00",
  "stock": 10,
  "is_available": true
}
```

- Success response: `200 OK`
- Error responses:
  - `401 Unauthorized` when no valid token is sent
  - `403 Forbidden` when another user tries to edit the menu item

### Delete Menu Item

- Method: `DELETE`
- URL: `/api/menu-items/<id>/`
- Auth required: Yes, and the authenticated user must be the creator
- Request body: None
- Success response: `204 No Content`
- Error responses:
  - `401 Unauthorized` when no valid token is sent
  - `403 Forbidden` when another user tries to delete the menu item

## Menu Categories

### List Menu Categories

- Method: `GET`
- URL: `/api/menu-categories/`
- Auth required: No
- Request body: None
- Success response: `200 OK`

```json
[
  {
    "id": 1,
    "name": "Rice",
    "description": "Rice meals",
    "menu_item_count": 1,
    "menu_items": [
      {
        "id": 1,
        "menu_category": {
          "id": 1,
          "name": "Rice",
          "description": "Rice meals"
        },
        "created_by": {
          "id": 2,
          "username": "chef"
        },
        "name": "Jollof Rice",
        "description": "Party-style jollof rice",
        "price": "2500.00",
        "stock": 12,
        "is_available": true,
        "image": null,
        "created_at": "2026-05-18T09:00:00Z"
      }
    ]
  }
]
```
