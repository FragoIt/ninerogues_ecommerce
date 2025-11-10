# Documentación de API - NineRogues E-Commerce

## 📋 Información General

**Base URL Desarrollo:** `http://localhost:8000`
**Base URL Producción:** `https://tu-dominio.com`

**Formato de Respuesta:** JSON
**Autenticación:** JWT (JSON Web Tokens)

---

## 🔐 Autenticación

Todos los endpoints protegidos requieren el header:
```
Authorization: JWT <access_token>
```

### Obtener Token (Login)

**Endpoint:** `POST /auth/jwt/create/`

**Body:**
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token

**Endpoint:** `POST /auth/jwt/refresh/`

**Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Respuesta (200):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Registro de Usuario

**Endpoint:** `POST /auth/users/`

**Body:**
```json
{
  "email": "nuevo@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "password": "contraseña_segura_123",
  "re_password": "contraseña_segura_123"
}
```

**Respuesta (201):**
```json
{
  "email": "nuevo@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "id": 5
}
```

### Activar Cuenta

**Endpoint:** `POST /auth/users/activation/`

**Body:**
```json
{
  "uid": "MQ",
  "token": "5wq-ae5c24..."
}
```

### Obtener Usuario Actual

**Endpoint:** `GET /auth/users/me/`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

### Reset Password

**Solicitar Reset:**
```
POST /auth/users/reset_password/
Body: {"email": "usuario@ejemplo.com"}
```

**Confirmar Reset:**
```
POST /auth/users/reset_password_confirm/
Body: {
  "uid": "MQ",
  "token": "5wq-ae5c24...",
  "new_password": "nueva_contraseña_123",
  "re_new_password": "nueva_contraseña_123"
}
```

---

## 📦 Productos

### Listar Productos

**Endpoint:** `GET /api/product/`

**Query Parameters:**
- `page` - Número de página (default: 1)
- `page_size` - Items por página (default: 10)

**Respuesta (200):**
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/product/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Producto Ejemplo",
      "description": "Descripción del producto...",
      "price": "99.99",
      "compare_price": "129.99",
      "photo": "http://localhost:8000/media/photos/2024/01/producto.jpg",
      "category": {
        "id": 1,
        "name": "Electrónicos",
        "slug": "electronicos"
      },
      "quantity": 50,
      "sold": 25,
      "date_created": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Detalle de Producto

**Endpoint:** `GET /api/product/{id}/`

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Producto Ejemplo",
  "description": "Descripción completa del producto...",
  "price": "99.99",
  "compare_price": "129.99",
  "photo": "http://localhost:8000/media/photos/2024/01/producto.jpg",
  "category": {
    "id": 1,
    "name": "Electrónicos",
    "slug": "electronicos"
  },
  "quantity": 50,
  "sold": 25,
  "date_created": "2024-01-15T10:30:00Z"
}
```

### Buscar Productos

**Endpoint:** `GET /api/product/search`

**Query Parameters:**
- `search` - Término de búsqueda (requerido)
- `category_id` - Filtrar por categoría (opcional)
- `min_price` - Precio mínimo (opcional)
- `max_price` - Precio máximo (opcional)

**Ejemplo:**
```
GET /api/product/search?search=laptop&category_id=1&min_price=500&max_price=2000
```

---

## 🏷️ Categorías

### Listar Categorías

**Endpoint:** `GET /api/category/`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "Electrónicos",
    "slug": "electronicos"
  },
  {
    "id": 2,
    "name": "Ropa",
    "slug": "ropa"
  }
]
```

---

## 🛒 Carrito

### Obtener Carrito

**Endpoint:** `GET /api/cart/`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
{
  "items": [
    {
      "id": 1,
      "product": {
        "id": 5,
        "name": "Laptop HP",
        "price": "799.99",
        "photo": "..."
      },
      "count": 2
    }
  ],
  "amount": "1599.98",
  "compare_amount": "2199.98",
  "total_items": 2
}
```

### Añadir al Carrito

**Endpoint:** `POST /api/cart/add-item`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "product_id": 5,
  "count": 2
}
```

**Respuesta (200):**
```json
{
  "items": [...],
  "amount": "1599.98",
  "total_items": 2
}
```

### Actualizar Item

**Endpoint:** `PUT /api/cart/update-item`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "product_id": 5,
  "count": 3
}
```

### Eliminar Item

**Endpoint:** `DELETE /api/cart/remove-item`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "product_id": 5
}
```

### Vaciar Carrito

**Endpoint:** `DELETE /api/cart/empty-cart`

**Headers:** `Authorization: JWT <token>`

### Sincronizar Carrito

**Endpoint:** `GET /api/cart/synch`

**Headers:** `Authorization: JWT <token>`

---

## ❤️ Wishlist

### Obtener Wishlist

**Endpoint:** `GET /api/wishlist/`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
{
  "wishlist": [
    {
      "id": 1,
      "product": {
        "id": 10,
        "name": "Smartwatch",
        "price": "299.99",
        "photo": "..."
      }
    }
  ],
  "total_items": 1
}
```

### Añadir a Wishlist

**Endpoint:** `POST /api/wishlist/add-item`

**Body:**
```json
{
  "product_id": 10
}
```

### Eliminar de Wishlist

**Endpoint:** `DELETE /api/wishlist/remove-item`

**Body:**
```json
{
  "product_id": 10
}
```

---

## 🚚 Envío

### Obtener Opciones de Envío

**Endpoint:** `GET /api/shipping/`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "Envío Estándar",
    "time_to_delivery": "5-7 días",
    "price": "5.99"
  },
  {
    "id": 2,
    "name": "Envío Express",
    "time_to_delivery": "2-3 días",
    "price": "12.99"
  }
]
```

---

## 🎟️ Cupones

### Validar Cupón

**Endpoint:** `POST /api/coupons/check`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "coupon_name": "SAVE20"
}
```

**Respuesta Exitosa (200):**
```json
{
  "coupon": {
    "name": "SAVE20",
    "discount_percentage": 20
  }
}
```

**Respuesta Error (404):**
```json
{
  "error": "Cupón no válido"
}
```

---

## 💳 Pago

### Obtener Token de Braintree

**Endpoint:** `GET /api/payment/get-token`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
{
  "braintree_token": "eyJ2ZXJzaW9uIjoyLCJhdXRob3JpemF0aW9uRmluZ2VycHJpbnQi..."
}
```

### Calcular Total de Pago

**Endpoint:** `GET /api/payment/get-payment-total`

**Headers:** `Authorization: JWT <token>`

**Query Parameters:**
- `shipping_id` - ID de opción de envío (requerido)
- `coupon_name` - Nombre del cupón (opcional)

**Ejemplo:**
```
GET /api/payment/get-payment-total?shipping_id=1&coupon_name=SAVE20
```

**Respuesta (200):**
```json
{
  "original_price": "1599.98",
  "total_after_coupon": "1279.98",
  "estimated_tax": "230.40",
  "shipping_cost": "5.99",
  "total_amount": "1516.37"
}
```

### Procesar Pago

**Endpoint:** `POST /api/payment/process`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "nonce": {
    "nonce": "tokencc_bh_s3bgkw_ghq7jq_6qw8wc_yt8tcd_5g4"
  },
  "shipping_id": 1,
  "coupon_name": "SAVE20",
  "full_name": "Juan Pérez",
  "address_line_1": "Calle Principal 123",
  "address_line_2": "Apt 4B",
  "city": "Lima",
  "state_province_region": "Lima",
  "postal_zip_code": "15001",
  "country_region": "PE",
  "telephone_number": "+51999123456"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": "Transaction successful and order was created"
}
```

**Respuesta Error:**
```json
{
  "error": "Not enough items in stock"
}
```

---

## 📋 Órdenes

### Listar Órdenes del Usuario

**Endpoint:** `GET /api/orders/`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "transaction_id": "abc123xyz",
    "amount": "1516.37",
    "status": "processed",
    "full_name": "Juan Pérez",
    "address_line_1": "Calle Principal 123",
    "city": "Lima",
    "country_region": "PE",
    "shipping_name": "Envío Estándar",
    "shipping_time": "5-7 días",
    "date_issued": "2024-01-15T14:30:00Z"
  }
]
```

### Detalle de Orden

**Endpoint:** `GET /api/orders/{id}/`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
{
  "id": 1,
  "transaction_id": "abc123xyz",
  "amount": "1516.37",
  "status": "processed",
  "full_name": "Juan Pérez",
  "address_line_1": "Calle Principal 123",
  "address_line_2": "Apt 4B",
  "city": "Lima",
  "state_province_region": "Lima",
  "postal_zip_code": "15001",
  "country_region": "PE",
  "telephone_number": "+51999123456",
  "shipping_name": "Envío Estándar",
  "shipping_time": "5-7 días",
  "shipping_price": "5.99",
  "date_issued": "2024-01-15T14:30:00Z",
  "items": [
    {
      "id": 1,
      "name": "Laptop HP",
      "price": "799.99",
      "count": 2,
      "product": {
        "id": 5,
        "photo": "..."
      }
    }
  ]
}
```

---

## ⭐ Reviews

### Obtener Reviews de Producto

**Endpoint:** `GET /api/reviews/{product_id}`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "user": {
      "first_name": "María",
      "last_name": "González"
    },
    "rating": "4.5",
    "comment": "Excelente producto, muy recomendado!",
    "date_created": "2024-01-10T10:00:00Z"
  }
]
```

### Crear Review

**Endpoint:** `POST /api/reviews/create`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "product_id": 5,
  "rating": "4.5",
  "comment": "Excelente producto, muy recomendado!"
}
```

**Respuesta (201):**
```json
{
  "id": 1,
  "rating": "4.5",
  "comment": "Excelente producto, muy recomendado!",
  "date_created": "2024-01-15T15:00:00Z"
}
```

### Actualizar Review

**Endpoint:** `PUT /api/reviews/{id}`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "rating": "5.0",
  "comment": "Actualicé mi opinión, producto perfecto!"
}
```

### Eliminar Review

**Endpoint:** `DELETE /api/reviews/{id}`

**Headers:** `Authorization: JWT <token>`

---

## 👤 Perfil de Usuario

### Obtener Perfil

**Endpoint:** `GET /api/profile/`

**Headers:** `Authorization: JWT <token>`

**Respuesta (200):**
```json
{
  "address_line_1": "Calle Principal 123",
  "address_line_2": "Apt 4B",
  "city": "Lima",
  "state_province_region": "Lima",
  "postal_zip_code": "15001",
  "country_region": "PE",
  "telephone_number": "+51999123456"
}
```

### Actualizar Perfil

**Endpoint:** `PUT /api/profile/update`

**Headers:** `Authorization: JWT <token>`

**Body:**
```json
{
  "address_line_1": "Nueva Dirección 456",
  "city": "Lima",
  "country_region": "PE",
  "telephone_number": "+51999654321"
}
```

---

## 📊 Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Eliminación exitosa
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 🔍 Ejemplos con cURL

### Login
```bash
curl -X POST http://localhost:8000/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@ejemplo.com",
    "password": "contraseña123"
  }'
```

### Obtener Productos (con autenticación)
```bash
curl -X GET http://localhost:8000/api/product/ \
  -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Añadir al Carrito
```bash
curl -X POST http://localhost:8000/api/cart/add-item \
  -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 5,
    "count": 2
  }'
```

---

## 📝 Notas Importantes

1. **Rate Limiting:** Implementar rate limiting en producción
2. **Pagination:** Todas las listas están paginadas
3. **CORS:** Configurar origins permitidos en producción
4. **HTTPS:** Usar HTTPS en producción
5. **Tokens:** Los tokens JWT expiran (configurar refresh)

---

## 🚀 Próximas Mejoras de API

- [ ] Versionado de API (v1, v2)
- [ ] OpenAPI/Swagger documentation
- [ ] GraphQL endpoint (opcional)
- [ ] Webhooks para eventos
- [ ] Rate limiting por usuario
- [ ] API Keys para integraciones
- [ ] Respuestas en múltiples idiomas

---

**Última Actualización:** 2025-11-10
**Versión API:** 1.0.0
