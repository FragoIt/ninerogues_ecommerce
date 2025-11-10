# Arquitectura Técnica - NineRogues E-Commerce

## 🏛️ Visión General de la Arquitectura

NineRogues implementa una arquitectura **cliente-servidor desacoplada** con:
- **Backend:** API RESTful con Django REST Framework
- **Frontend:** SPA (Single Page Application) con React
- **Comunicación:** HTTP/JSON sobre CORS

```
┌─────────────────────────────────────────────────────────────┐
│                     Cliente (Browser)                        │
│  ┌────────────────────────────────────────────────────┐     │
│  │            React SPA (Port 3000)                   │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐    │     │
│  │  │Components│  │ Containers│  │Redux Store   │    │     │
│  │  └─────┬────┘  └─────┬────┘  └──────┬───────┘    │     │
│  │        │             │                │            │     │
│  │        └─────────────┴────────────────┘            │     │
│  │                      │                              │     │
│  │                 Axios Requests                      │     │
│  └──────────────────────┼──────────────────────────────┘     │
└─────────────────────────┼─────────────────────────────────────┘
                          │ CORS
                          │ HTTP/JSON
┌─────────────────────────┼─────────────────────────────────────┐
│                         │                                      │
│  ┌──────────────────────▼──────────────────────────────┐      │
│  │        Django REST API (Port 8000)                  │      │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐     │      │
│  │  │  Views   │  │Serializers│  │  Models      │     │      │
│  │  └────┬─────┘  └─────┬────┘  └──────┬───────┘     │      │
│  │       │              │                │             │      │
│  │       └──────────────┴────────────────┘             │      │
│  └──────────────────────┼───────────────────────────────┘      │
│                         │                                      │
│  ┌──────────────────────▼───────────────────────────────┐     │
│  │              PostgreSQL Database                      │     │
│  │    ┌─────────┬──────────┬────────┬──────────┐       │     │
│  │    │Products │ Orders   │ Users  │ Reviews  │       │     │
│  │    └─────────┴──────────┴────────┴──────────┘       │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                                │
│  ┌──────────────────────────────────────────────────────┐     │
│  │            Servicios Externos                        │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐      │     │
│  │  │Braintree │  │  AWS S3  │  │ Email (SMTP) │      │     │
│  │  └──────────┘  └──────────┘  └──────────────┘      │     │
│  └──────────────────────────────────────────────────────┘     │
│                     Backend (Server)                          │
└───────────────────────────────────────────────────────────────┘
```

## 📦 Estructura de Módulos Backend

### Modelo de Apps Django

El proyecto sigue el patrón de **apps modulares** de Django:

```python
apps/
├── user/              # Usuario base (extiende AbstractBaseUser)
├── user_profile/      # Perfil extendido del usuario
├── category/          # Categorías de productos
├── product/           # Productos (core)
├── cart/              # Carrito de compras
├── wishlist/          # Lista de deseos
├── shipping/          # Opciones de envío
├── coupons/           # Sistema de cupones
├── payment/           # Procesamiento de pagos
├── orders/            # Gestión de órdenes
└── reviews/           # Sistema de reseñas
```

### Relaciones Entre Modelos

```
User (Django Auth)
  │
  ├──► UserProfile (OneToOne)
  │     └── address_line_1, city, country, etc.
  │
  ├──► Cart (OneToOne)
  │     └──► CartItem (Many)
  │           └──► Product (FK)
  │
  ├──► WishList (OneToOne)
  │     └──► WishListItem (Many)
  │           └──► Product (FK)
  │
  ├──► Order (Many)
  │     ├──► OrderItem (Many)
  │     │     └──► Product (FK)
  │     └── Shipping info, payment info
  │
  └──► Review (Many)
        └──► Product (FK)

Category
  └──► Product (Many)
        ├── price, compare_price
        ├── quantity, sold
        └── photo

FixedPriceCoupon / PercentageCoupon
  (validados en checkout)

Shipping
  (opciones de envío disponibles)
```

## 🔄 Flujo de Datos

### 1. Flujo de Autenticación

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  React   │────────>│ Djoser   │────────>│ Database │
│          │  POST   │ API      │  Query  │          │
└──────────┘ /auth/  └──────────┘         └──────────┘
              jwt/create/
                │
                ▼
         Return JWT Token
                │
                ▼
    Store in Redux + localStorage
                │
                ▼
    Include in all API requests
    Header: Authorization: JWT {token}
```

### 2. Flujo de Compra (Checkout)

```
Usuario en Checkout
       │
       ▼
1. GET /api/shipping/           # Obtener opciones de envío
       │
       ▼
2. POST /api/coupons/check      # Validar cupón (opcional)
       │
       ▼
3. GET /api/payment/get-payment-total  # Calcular total
       │                                # (productos + tax + shipping - coupon)
       ▼
4. GET /api/payment/get-token   # Obtener Braintree token
       │
       ▼
5. [Usuario completa pago en Braintree UI]
       │
       ▼
6. POST /api/payment/process    # Procesar pago
       │                        # {nonce, shipping, address, coupon}
       ├──> Validar stock
       ├──> Procesar pago (Braintree)
       ├──> Crear Order
       ├──> Crear OrderItems
       ├──> Actualizar inventario (quantity, sold)
       ├──> Enviar email confirmación
       └──> Vaciar carrito
       │
       ▼
   Redirect a /thankyou
```

### 3. Flujo de Carrito

```
┌─────────────────────────────────────────────┐
│ Redux State: cart                           │
│  {                                          │
│    items: [                                 │
│      {product, count},                      │
│      ...                                    │
│    ],                                       │
│    amount: 100.00,                         │
│    compare_amount: 150.00,                 │
│    total_items: 3                          │
│  }                                          │
└─────────────────────────────────────────────┘
         ▲                    │
         │                    │
    Redux Actions         API Calls
         │                    │
         ▼                    ▼
┌──────────────┐      ┌──────────────┐
│ add_item     │─────>│ POST /cart   │
│ update_item  │─────>│ PUT /cart    │
│ remove_item  │─────>│ DELETE /cart │
│ get_items    │<─────│ GET /cart    │
└──────────────┘      └──────────────┘
```

## 🎨 Estructura Frontend (React)

### Patrón de Componentes

```
src/
├── App.js                    # Router principal
├── store.js                  # Configuración Redux store
│
├── components/               # Componentes reutilizables
│   ├── cart/
│   │   ├── CartItem.js      # Individual item en carrito
│   │   └── WishlistItem.js
│   ├── checkout/
│   │   └── ShippingForm.js  # Formulario de dirección
│   ├── navigation/
│   │   ├── Navbar.js
│   │   ├── Footer.js
│   │   └── SearchBox.js
│   └── product/
│       ├── ProductCard.js   # Card de producto
│       ├── ImageGallery.js
│       ├── Stars.js         # Rating visual
│       └── WishlistHeart.js # Botón agregar a wishlist
│
├── containers/               # Páginas completas (connected to Redux)
│   ├── Home.js
│   ├── Shop.js
│   ├── auth/
│   │   ├── Login.js
│   │   ├── Signup.js
│   │   └── Activate.js
│   └── pages/
│       ├── Cart.js
│       ├── Checkout.js
│       ├── ProductDetail.js
│       ├── Dashboard.js
│       └── ThankYou.js
│
└── redux/
    ├── actions/              # Action creators
    │   ├── auth.js          # login, signup, load_user
    │   ├── cart.js          # add_item, remove_item
    │   ├── products.js      # get_products, get_product
    │   ├── orders.js        # get_orders, get_order_detail
    │   └── ...
    │
    └── reducers/             # State management
        ├── index.js         # combineReducers
        ├── auth.js          # {isAuthenticated, user, loading}
        ├── cart.js          # {items, amount, total_items}
        ├── products.js      # {products, product, filtered}
        └── ...
```

### Redux State Shape

```javascript
{
  auth: {
    access: "jwt_token",
    refresh: "refresh_token",
    isAuthenticated: true,
    user: {
      id: 1,
      email: "user@example.com",
      first_name: "John",
      last_name: "Doe"
    }
  },
  cart: {
    items: [...],
    amount: 100.00,
    compare_amount: 150.00,
    total_items: 3
  },
  products: {
    products: [...],
    product: {...},
    filtered_products: [...],
    search_products: [...]
  },
  orders: {
    orders: [...],
    order: {...}
  },
  reviews: {
    reviews: [...]
  },
  wishlist: {
    items: [...],
    total_items: 5
  },
  categories: {
    categories: [...]
  },
  shipping: {
    shipping: [...]
  },
  coupons: {
    coupon: {...}
  },
  payment: {
    braintree_token: "...",
    made_payment: false,
    loading: false
  }
}
```

## 🔌 API Endpoints

### Authentication (Djoser)
```
POST   /auth/users/                    # Registro
POST   /auth/users/activation/         # Activar cuenta
POST   /auth/jwt/create/               # Login (obtener JWT)
POST   /auth/jwt/refresh/              # Refresh token
POST   /auth/users/reset_password/     # Solicitar reset
POST   /auth/users/reset_password_confirm/  # Confirmar reset
GET    /auth/users/me/                 # Usuario actual
```

### Products
```
GET    /api/product/                   # Lista de productos
GET    /api/product/{id}               # Detalle de producto
GET    /api/product/get-products       # Productos filtrados
GET    /api/product/search             # Búsqueda
POST   /api/product/ (admin)           # Crear producto
PUT    /api/product/{id} (admin)       # Actualizar producto
DELETE /api/product/{id} (admin)       # Eliminar producto
```

### Categories
```
GET    /api/category/                  # Lista categorías
```

### Cart
```
GET    /api/cart/                      # Obtener carrito
POST   /api/cart/add-item              # Agregar item
PUT    /api/cart/update-item           # Actualizar cantidad
DELETE /api/cart/remove-item           # Eliminar item
DELETE /api/cart/empty-cart            # Vaciar carrito
GET    /api/cart/synch                 # Sincronizar carrito
```

### Wishlist
```
GET    /api/wishlist/                  # Obtener wishlist
POST   /api/wishlist/add-item          # Agregar item
DELETE /api/wishlist/remove-item       # Eliminar item
GET    /api/wishlist/items             # Items en wishlist
```

### Orders
```
GET    /api/orders/                    # Lista de órdenes del usuario
GET    /api/orders/{id}                # Detalle de orden
```

### Payment
```
GET    /api/payment/get-token          # Token Braintree
GET    /api/payment/get-payment-total  # Calcular total
POST   /api/payment/process            # Procesar pago
```

### Shipping
```
GET    /api/shipping/                  # Opciones de envío
```

### Coupons
```
POST   /api/coupons/check              # Validar cupón
```

### Reviews
```
GET    /api/reviews/{product_id}       # Reviews de producto
POST   /api/reviews/create             # Crear review
PUT    /api/reviews/{id}               # Actualizar review
DELETE /api/reviews/{id}               # Eliminar review
GET    /api/reviews/get-review/{id}    # Review específica
```

## 🔒 Seguridad

### Backend (Django)
1. **Autenticación JWT:** SimpleJWT via Djoser
2. **CORS:** django-cors-headers (configurado para dominio específico)
3. **Passwords:** Hasheadas con Argon2
4. **CSRF:** Token CSRF en forms
5. **SQL Injection:** ORM de Django (protegido)
6. **XSS:** Templates de Django (escapado automático)

### Frontend (React)
1. **JWT Storage:** localStorage (considerar httpOnly cookies)
2. **Input Validation:** Validación en formularios
3. **HTTPS Only:** En producción
4. **No Secrets:** Variables de entorno para API keys

### Consideraciones
⚠️ **Vulnerabilidades a Atender:**
- Actualizar Django (versión con CVEs conocidos)
- Actualizar Pillow (vulnerabilidades de imagen)
- Implementar rate limiting
- Añadir CAPTCHA en forms críticos
- Implementar 2FA
- Logging de acciones sensibles

## ⚡ Performance

### Backend
- **Database:** PostgreSQL con índices en FKs
- **Static Files:** WhiteNoise para servir archivos estáticos
- **Media Files:** AWS S3 en producción
- **Serialización:** Django REST Framework serializers
- **Queries:** ORM Django (potencial para optimizar con select_related)

### Frontend
- **Bundle:** Create React App (webpack)
- **Code Splitting:** React.lazy (no implementado aún)
- **State Management:** Redux (overhead, considerar Context API)
- **Imágenes:** Sin optimización (añadir lazy loading)
- **Caching:** Service Worker (implementado)

### Oportunidades de Optimización
1. Implementar Redis para cache
2. Usar select_related/prefetch_related en queries complejas
3. Pagination en listas largas
4. Lazy loading de imágenes
5. CDN para assets
6. Compresión Gzip/Brotli
7. Database connection pooling
8. Query optimization (Django Debug Toolbar)

## 🚀 Deployment

### Arquitectura de Producción Recomendada

```
Internet
   │
   ▼
[Cloudflare/CDN]
   │
   ▼
[Load Balancer]
   │
   ├─────────────┬─────────────┐
   ▼             ▼             ▼
[Web Server] [Web Server] [Web Server]
 (Gunicorn)   (Gunicorn)   (Gunicorn)
   │             │             │
   └─────────────┴─────────────┘
                 │
                 ▼
        [PostgreSQL Database]
         (Master + Replicas)
                 │
                 ▼
        [Redis Cache]
                 │
                 ▼
        [AWS S3] (Media Files)
```

### Configuración Actual (Single Server)
```
[Render/Heroku]
  ├── Django (Gunicorn)
  ├── Static Files (WhiteNoise)
  └── PostgreSQL
  
[AWS S3]
  └── Media Files (user uploads)

[Braintree]
  └── Payment Processing
```

## 📊 Monitoreo y Observabilidad

### Actualmente No Implementado
- [ ] Application Performance Monitoring (APM)
- [ ] Error Tracking (Sentry)
- [ ] Logging centralizado
- [ ] Métricas de negocio
- [ ] Health checks
- [ ] Alertas

### Recomendaciones
1. **Sentry:** Para tracking de errores
2. **New Relic/DataDog:** Para APM
3. **Google Analytics:** Para métricas de usuario
4. **Prometheus + Grafana:** Para métricas de sistema
5. **ELK Stack:** Para logs centralizados

## 🧪 Testing Strategy (Propuesta)

### Actualmente: 0% Coverage

### Estrategia Propuesta:

```
1. Unit Tests (70% coverage target)
   ├── Models
   ├── Serializers
   ├── Utilities
   └── Business Logic

2. Integration Tests (20% coverage)
   ├── API Endpoints
   ├── Authentication Flow
   └── Payment Flow

3. E2E Tests (10% coverage)
   ├── User Registration
   ├── Complete Purchase Flow
   └── Admin Operations
```

### Tools Recomendadas
- **Backend:** pytest-django, factory-boy, coverage
- **Frontend:** Jest, React Testing Library, Cypress
- **API:** Postman/Newman, pytest-django

## 📚 Patrones de Diseño Utilizados

### Backend
1. **MVT (Model-View-Template):** Arquitectura Django
2. **Repository Pattern:** Django ORM como repository
3. **Serializer Pattern:** DRF Serializers
4. **ViewSet Pattern:** DRF ViewSets
5. **Signal Pattern:** Django signals (no usado extensivamente)

### Frontend
1. **Component-Based:** React components
2. **Flux Pattern:** Redux
3. **Container/Presentational:** Containers vs Components
4. **HOC (Higher-Order Components):** No usado extensivamente
5. **Custom Hooks:** Potencial para implementar

## 🔧 Herramientas de Desarrollo

### Backend
- **Django Debug Toolbar:** Para profiling (recomendado)
- **django-extensions:** Para comandos útiles (recomendado)
- **ipdb:** Para debugging
- **flake8/black:** Para linting y formatting

### Frontend
- **React DevTools:** Extension de browser
- **Redux DevTools:** Extension de browser (ya configurado)
- **ESLint:** Configurado en CRA
- **Prettier:** Recomendado añadir

## 📈 Métricas Clave a Monitorear

### Técnicas
- Tiempo de respuesta API (< 200ms)
- Tasa de errores (< 1%)
- Uptime (> 99.9%)
- Database query time
- Memory/CPU usage

### Negocio
- Tasa de conversión
- Abandono de carrito
- Valor promedio de orden (AOV)
- Customer Lifetime Value (CLV)
- Retención de usuarios
- Productos más vendidos

---

**Última actualización:** 2025
**Mantenido por:** DevOps Team
