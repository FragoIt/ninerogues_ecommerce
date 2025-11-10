# 🚀 Quick Start Guide - NineRogues E-Commerce

Esta guía te ayudará a tener el proyecto corriendo en **menos de 15 minutos**.

---

## ⚡ Requisitos Rápidos

Asegúrate de tener instalado:
- ✅ Python 3.8+ 
- ✅ Node.js 14+
- ✅ PostgreSQL
- ✅ Git

---

## 🏃 Inicio Rápido (5 Pasos)

### 1️⃣ Clonar y Navegar

```bash
git clone https://github.com/FragoIt/ninerogues_ecommerce.git
cd ninerogues_ecommerce
```

### 2️⃣ Backend Setup (Terminal 1)

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Mac/Linux)
source venv/bin/activate
# O en Windows
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos PostgreSQL
createdb ninerogues_db

# Crear archivo .env (ver abajo)
nano .env

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

**Archivo .env mínimo:**
```bash
SECRET_KEY=tu-secret-key-muy-larga-y-segura-minimo-50-caracteres-aqui
DEBUG=True
DOMAIN=http://localhost:3000
DATABASE_URL=postgres://postgres:password@localhost/ninerogues_db
BT_ENVIRONMENT=Sandbox
BT_MERCHANT_ID=tu_merchant_id
BT_PUBLIC_KEY=tu_public_key
BT_PRIVATE_KEY=tu_private_key
```

### 3️⃣ Frontend Setup (Terminal 2)

```bash
# En la misma carpeta del proyecto
npm install

# Ejecutar servidor React
npm start
```

### 4️⃣ Crear Datos de Prueba

**Via Django Admin:**
1. Ve a `http://localhost:8000/admin`
2. Login con tu superusuario
3. Crea:
   - 2-3 Categorías
   - 5-10 Productos
   - 2 Opciones de Envío
   - 1-2 Cupones

**O via Django Shell (más rápido):**

```bash
python manage.py shell
```

```python
from apps.category.models import Category
from apps.product.models import Product
from apps.shipping.models import Shipping
from apps.coupons.models import PercentageCoupon
from decimal import Decimal

# Categorías
cat1 = Category.objects.create(name='Electrónicos', slug='electronicos')
cat2 = Category.objects.create(name='Ropa', slug='ropa')

# Productos
Product.objects.create(
    name='Laptop HP',
    description='Laptop profesional con 16GB RAM',
    price=Decimal('799.99'),
    compare_price=Decimal('999.99'),
    category=cat1,
    quantity=50
)

Product.objects.create(
    name='Camisa Premium',
    description='Camisa de algodón premium',
    price=Decimal('49.99'),
    compare_price=Decimal('79.99'),
    category=cat2,
    quantity=100
)

# Envíos
Shipping.objects.create(
    name='Envío Estándar',
    time_to_delivery='5-7 días',
    price=Decimal('5.99')
)

Shipping.objects.create(
    name='Envío Express',
    time_to_delivery='2-3 días',
    price=Decimal('12.99')
)

# Cupones
PercentageCoupon.objects.create(
    name='WELCOME20',
    discount_percentage=20
)

print("✅ Datos de prueba creados!")
exit()
```

### 5️⃣ ¡Listo! Abre tu Navegador

- **Frontend:** http://localhost:3000
- **Admin Panel:** http://localhost:8000/admin
- **API:** http://localhost:8000/api/product/

---

## 🎯 Flujo de Prueba Completo

### Paso 1: Registro e Inicio de Sesión

1. Abre http://localhost:3000
2. Click en "Sign Up"
3. Registra una cuenta
4. Activa la cuenta (en desarrollo, revisa la consola del servidor Django para el link de activación)
5. Login con tu cuenta

### Paso 2: Explorar Productos

1. Ve a "Shop" en el navbar
2. Explora los productos que creaste
3. Click en un producto para ver detalles

### Paso 3: Añadir al Carrito

1. Desde detalle del producto, añade al carrito
2. Añade 2-3 productos más
3. Click en el icono del carrito

### Paso 4: Wishlist

1. Desde un producto, click en el corazón para añadir a wishlist
2. Ve a tu wishlist desde el navbar

### Paso 5: Checkout (Sin Pago Real)

Para testing sin Braintree configurado:

1. Ve al carrito
2. Click en "Checkout"
3. Llena el formulario de envío
4. Prueba un cupón (ej: `WELCOME20`)
5. Verás el cálculo de precios

**Nota:** Para completar un pago real, necesitas configurar Braintree Sandbox.

### Paso 6: Dashboard

1. Ve a tu Dashboard desde el navbar
2. Explora:
   - Profile settings
   - Order history (vacío si no completaste un pago)

---

## 🐛 Solución Rápida de Problemas

### Error: "No module named X"
```bash
pip install -r requirements.txt
```

### Error: Puerto 8000 en uso
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# O usa otro puerto
python manage.py runserver 8001
```

### Error: "database does not exist"
```bash
createdb ninerogues_db
python manage.py migrate
```

### Error: "Module not found" en React
```bash
rm -rf node_modules
npm install
```

### Imágenes no se cargan
En desarrollo sin S3, asegúrate de tener en `core/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # tus urls...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🔐 Configurar Braintree Sandbox (Opcional)

Para testing de pagos reales:

1. **Crear cuenta:** https://sandbox.braintreegateway.com/login
2. **Obtener credenciales:** Settings > API Keys
3. **Añadir a .env:**
   ```
   BT_ENVIRONMENT=Sandbox
   BT_MERCHANT_ID=tu_merchant_id_aqui
   BT_PUBLIC_KEY=tu_public_key_aqui
   BT_PRIVATE_KEY=tu_private_key_aqui
   ```
4. **Reiniciar servidor Django**

**Tarjetas de prueba Braintree:**
- Visa: `4111 1111 1111 1111`
- Mastercard: `5555 5555 5555 4444`
- CVV: `123`
- Fecha: Cualquier fecha futura

---

## 📊 Comandos Útiles

### Django

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Django shell
python manage.py shell

# Recopilar archivos estáticos
python manage.py collectstatic

# Ejecutar tests (cuando se implementen)
python manage.py test
```

### React

```bash
# Iniciar dev server
npm start

# Build para producción
npm run build

# Ejecutar tests
npm test

# Ver bundle size
npm run build -- --stats
```

### Database

```bash
# Backup de base de datos
pg_dump ninerogues_db > backup.sql

# Restore de backup
psql ninerogues_db < backup.sql

# Conectar a base de datos
psql ninerogues_db
```

---

## 🎨 Personalización Rápida

### Cambiar Branding

**Logo y Nombre:**
1. Edita `src/components/navigation/Navbar.js`
2. Reemplaza "NineRogues" con tu nombre
3. Añade tu logo en `public/logo.png`

**Colores (Tailwind):**
Edita `tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#tu-color-primario',
        secondary: '#tu-color-secundario',
      }
    }
  }
}
```

**Favicon:**
Reemplaza `public/favicon.ico`

---

## 📚 Próximos Pasos

Una vez que tengas todo corriendo:

1. **Lee la documentación completa:**
   - [README.md](README.md) - Overview completo
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitectura técnica
   - [API.md](API.md) - Documentación de API
   - [SECURITY.md](SECURITY.md) - Consideraciones de seguridad

2. **Explora el código:**
   - Backend: `apps/` directory
   - Frontend: `src/` directory
   - Models: `apps/*/models.py`
   - Views: `apps/*/views.py`
   - Components: `src/components/`

3. **Planea tu implementación:**
   - [BUSINESS_STRATEGY.md](BUSINESS_STRATEGY.md) - Estrategia de negocio
   - Define tu nicho
   - Personaliza el diseño
   - Añade tus productos

4. **Mejora el proyecto:**
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Guía de contribución
   - Actualiza dependencias
   - Añade tests
   - Mejora la seguridad

---

## ✅ Checklist de Setup Completo

- [ ] Backend corriendo en puerto 8000
- [ ] Frontend corriendo en puerto 3000
- [ ] Base de datos creada y migrada
- [ ] Superusuario creado
- [ ] Al menos 3 productos de prueba creados
- [ ] Opciones de envío creadas
- [ ] Puedes registrarte como usuario
- [ ] Puedes añadir productos al carrito
- [ ] Admin panel accesible
- [ ] No hay errores en consola

---

## 🆘 ¿Necesitas Ayuda?

- **Documentación:** Lee [INSTALLATION.md](INSTALLATION.md) para guía detallada
- **Issues:** Crea un issue en GitHub con detalles del problema
- **Logs:** Revisa la consola del servidor Django y React para errores
- **Community:** Stack Overflow con tags `django` y `react`

---

## 🎉 ¡Felicitaciones!

Si llegaste hasta aquí, tienes un e-commerce completo corriendo localmente.

**Siguiente paso:** Explora el código, personalízalo y construye tu negocio! 🚀

---

**Tiempo estimado de setup:** 10-15 minutos
**Última actualización:** 2025-11-10
