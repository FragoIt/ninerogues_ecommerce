# Guía de Instalación - NineRogues E-Commerce

## 📋 Requisitos Previos

### Software Requerido

- **Python:** 3.8 o superior (recomendado 3.10+)
- **Node.js:** 14 o superior (recomendado 18 LTS)
- **PostgreSQL:** 12 o superior
- **npm:** 6 o superior
- **Git:** Para clonar el repositorio

### Cuentas Externas Necesarias

1. **Braintree Account**
   - Sandbox para desarrollo: https://sandbox.braintreegateway.com
   - Production: https://www.braintreepayments.com

2. **AWS S3** (opcional para desarrollo, necesario para producción)
   - Cuenta AWS: https://aws.amazon.com
   - Bucket S3 configurado

3. **Email Service** (opcional)
   - Gmail para desarrollo
   - SendGrid/Mailgun para producción

---

## 🚀 Instalación Rápida (Desarrollo Local)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/FragoIt/ninerogues_ecommerce.git
cd ninerogues_ecommerce
```

### Paso 2: Configurar Backend (Django)

#### 2.1. Crear Entorno Virtual

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### 2.2. Instalar Dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Nota:** Si encuentras errores con `psycopg2`, intenta:
```bash
pip install psycopg2-binary
```

#### 2.3. Configurar PostgreSQL

**Crear Base de Datos:**

```sql
-- En PostgreSQL shell (psql)
CREATE DATABASE ninerogues_db;
CREATE USER ninerogues_user WITH PASSWORD 'tu_password_seguro';
ALTER ROLE ninerogues_user SET client_encoding TO 'utf8';
ALTER ROLE ninerogues_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ninerogues_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ninerogues_db TO ninerogues_user;
```

**Alternativa con createdb:**
```bash
createdb ninerogues_db
```

#### 2.4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
# .env
SECRET_KEY=tu-secret-key-muy-segura-y-larga-aqui-minimo-50-caracteres
DEBUG=True
DOMAIN=http://localhost:3000

# Database
DATABASE_URL=postgres://ninerogues_user:tu_password_seguro@localhost/ninerogues_db

# Braintree (Sandbox)
BT_ENVIRONMENT=Sandbox
BT_MERCHANT_ID=tu_merchant_id
BT_PUBLIC_KEY=tu_public_key
BT_PRIVATE_KEY=tu_private_key

# Email (Gmail para desarrollo)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
EMAIL_USE_TLS=True

# AWS S3 (Opcional para desarrollo)
# AWS_ACCESS_KEY_ID=tu_aws_access_key
# AWS_SECRET_ACCESS_KEY=tu_aws_secret_key
# AWS_STORAGE_BUCKET_NAME=tu_bucket_name
# AWS_S3_REGION_NAME=us-east-1
```

**Generar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### 2.5. Configurar Django Settings

Editar `core/settings.py` para desarrollo local:

```python
# Asegurar que estas líneas estén presentes
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Para desarrollo local sin S3
if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

#### 2.6. Ejecutar Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 2.7. Crear Superusuario

```bash
python manage.py createsuperuser
```

Sigue las instrucciones para crear tu cuenta de admin.

#### 2.8. Cargar Datos Iniciales (Opcional)

**Crear categorías iniciales:**

```bash
python manage.py shell
```

```python
from apps.category.models import Category

categories = [
    {'name': 'Electrónicos', 'slug': 'electronicos'},
    {'name': 'Ropa', 'slug': 'ropa'},
    {'name': 'Hogar', 'slug': 'hogar'},
    {'name': 'Deportes', 'slug': 'deportes'},
    {'name': 'Libros', 'slug': 'libros'},
]

for cat in categories:
    Category.objects.get_or_create(**cat)

exit()
```

**O crear fixtures:**

```bash
# Después de añadir datos via admin
python manage.py dumpdata apps.category --indent 2 > fixtures/categories.json
python manage.py dumpdata apps.shipping --indent 2 > fixtures/shipping.json

# Para cargar fixtures
python manage.py loaddata fixtures/categories.json
python manage.py loaddata fixtures/shipping.json
```

#### 2.9. Iniciar Servidor Django

```bash
python manage.py runserver
```

Backend disponible en: `http://localhost:8000`
Admin panel: `http://localhost:8000/admin`

### Paso 3: Configurar Frontend (React)

#### 3.1. Instalar Dependencias

En una nueva terminal:

```bash
npm install
```

**Si hay errores de dependencias:**
```bash
npm install --legacy-peer-deps
```

#### 3.2. Configurar Variables de Entorno

El archivo `.env` en la raíz ya debería contener:

```bash
SKIP_PREFLIGHT_CHECK=true
REACT_APP_API_URL=http://localhost:8000
```

#### 3.3. Iniciar Servidor React

```bash
npm start
```

Frontend disponible en: `http://localhost:3000`

La aplicación se abrirá automáticamente en tu navegador.

---

## 🔧 Configuración Adicional

### Configurar Braintree

1. **Crear cuenta sandbox:** https://sandbox.braintreegateway.com
2. **Obtener credenciales:** Settings > API Keys
3. **Copiar** Merchant ID, Public Key, Private Key al `.env`

### Configurar AWS S3 (Producción)

1. **Crear bucket S3:**
   ```bash
   aws s3 mb s3://tu-bucket-name
   ```

2. **Configurar CORS:**
   ```json
   [
       {
           "AllowedHeaders": ["*"],
           "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
           "AllowedOrigins": ["*"],
           "ExposeHeaders": ["ETag"]
       }
   ]
   ```

3. **Crear IAM user** con permisos S3

4. **Añadir a .env:**
   ```bash
   AWS_ACCESS_KEY_ID=tu_key
   AWS_SECRET_ACCESS_KEY=tu_secret
   AWS_STORAGE_BUCKET_NAME=tu_bucket
   ```

### Configurar Email (Gmail)

1. **Habilitar 2FA** en tu cuenta Gmail
2. **Generar App Password:**
   - Google Account > Security > 2-Step Verification > App passwords
3. **Usar App Password** en EMAIL_HOST_PASSWORD

---

## 📊 Verificar Instalación

### Backend

```bash
# En terminal con Django
python manage.py check
python manage.py test apps  # Si hay tests
```

### Frontend

```bash
# En terminal con React
npm test -- --watchAll=false
```

### Verificar Endpoints API

```bash
# Usando curl
curl http://localhost:8000/api/category/
curl http://localhost:8000/api/product/

# O usar Postman/Insomnia
```

---

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'core'"

**Solución:** Asegúrate de estar en el directorio correcto y que el entorno virtual esté activado.

```bash
pwd  # Debe mostrar .../ninerogues_ecommerce
which python  # Debe mostrar .../venv/bin/python
```

### Error: "psycopg2 installation failed"

**Solución:**

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libpq-dev

# macOS
brew install postgresql

# Luego
pip install psycopg2-binary
```

### Error: "Port 8000 already in use"

**Solución:**

```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# O usar otro puerto
python manage.py runserver 8001
```

### Error: "Module not found" en React

**Solución:**

```bash
rm -rf node_modules package-lock.json
npm install
```

### Error de CORS en navegador

**Solución:** Verificar en `core/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Imágenes no se cargan

**Desarrollo local sin S3:**

Editar `core/urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... tus URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🏗️ Datos de Prueba

### Crear Productos de Prueba

**Via Django Admin:**
1. Ir a `http://localhost:8000/admin`
2. Login con superusuario
3. Añadir productos en "Products"

**Via Django Shell:**

```python
python manage.py shell

from apps.product.models import Product
from apps.category.models import Category
from decimal import Decimal

cat = Category.objects.first()

Product.objects.create(
    name="Producto de Prueba 1",
    description="Descripción del producto de prueba",
    price=Decimal('99.99'),
    compare_price=Decimal('129.99'),
    category=cat,
    quantity=100,
    sold=0
)
```

### Crear Opciones de Envío

```python
from apps.shipping.models import Shipping

Shipping.objects.create(
    name="Envío Estándar",
    time_to_delivery="5-7 días",
    price=Decimal('5.99')
)

Shipping.objects.create(
    name="Envío Express",
    time_to_delivery="2-3 días",
    price=Decimal('12.99')
)
```

### Crear Cupones

```python
from apps.coupons.models import FixedPriceCoupon, PercentageCoupon

# Cupón de descuento fijo
FixedPriceCoupon.objects.create(
    name="WELCOME10",
    discount_price=Decimal('10.00')
)

# Cupón de porcentaje
PercentageCoupon.objects.create(
    name="SAVE20",
    discount_percentage=20
)
```

---

## 🚀 Despliegue en Producción

### Preparación

1. **Actualizar settings para producción:**

```python
# core/settings.py
DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

2. **Generar archivos estáticos:**

```bash
python manage.py collectstatic --noinput
```

3. **Build del frontend:**

```bash
npm run build
```

### Opciones de Hosting

#### Opción 1: Render (Recomendado)

**Backend:**
1. Crear cuenta en Render.com
2. Nuevo Web Service
3. Conectar repositorio
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn core.wsgi:application`
6. Añadir variables de entorno
7. Añadir PostgreSQL database

**Frontend:**
1. Nuevo Static Site
2. Build Command: `npm run build`
3. Publish Directory: `build`

#### Opción 2: Heroku

```bash
# Instalar Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Crear app
heroku create tu-app-name

# Añadir PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variables
heroku config:set SECRET_KEY=tu_secret_key
heroku config:set DEBUG=False
# ... otras variables

# Deploy
git push heroku main

# Migrar
heroku run python manage.py migrate

# Crear superuser
heroku run python manage.py createsuperuser
```

#### Opción 3: Railway

Muy similar a Render, con UI intuitiva.

#### Opción 4: VPS (Digital Ocean, AWS EC2, etc.)

Requiere más configuración manual pero da más control.

---

## 📚 Recursos Adicionales

### Documentación

- **Django:** https://docs.djangoproject.com/
- **DRF:** https://www.django-rest-framework.org/
- **React:** https://react.dev/
- **Braintree:** https://developer.paypal.com/braintree/docs/

### Tutoriales Recomendados

- Django E-commerce: https://testdriven.io/
- React Shopping Cart: https://www.freecodecamp.org/
- Deployment: https://realpython.com/

### Comunidad

- Stack Overflow
- Django Discord
- Reddit r/django
- Reddit r/reactjs

---

## ✅ Checklist de Instalación Completa

### Backend
- [ ] Python 3.8+ instalado
- [ ] PostgreSQL instalado y corriendo
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Base de datos creada
- [ ] Variables de entorno configuradas
- [ ] Migraciones ejecutadas
- [ ] Superusuario creado
- [ ] Servidor corriendo en 8000

### Frontend
- [ ] Node.js 14+ instalado
- [ ] npm instalado
- [ ] Dependencias instaladas
- [ ] Variables de entorno configuradas
- [ ] Servidor corriendo en 3000
- [ ] Conecta con backend correctamente

### Datos Iniciales
- [ ] Categorías creadas
- [ ] Opciones de envío creadas
- [ ] Al menos 1 producto de prueba
- [ ] Cupones de prueba (opcional)

### Verificación
- [ ] Admin panel accesible
- [ ] Frontend carga correctamente
- [ ] Registro de usuario funciona
- [ ] Login funciona
- [ ] Productos se muestran
- [ ] Carrito funciona
- [ ] No hay errores en consola

---

## 🆘 Soporte

Si encuentras problemas:

1. **Revisar logs:**
   ```bash
   # Django
   python manage.py runserver --noreload

   # React
   npm start
   ```

2. **Revisar documentación** en esta carpeta

3. **GitHub Issues:** Crear issue con detalles

4. **Community:** Stack Overflow con tags `django` y `react`

---

**Última Actualización:** 2025-11-10
**Versión:** 1.0.0
**Mantenido por:** DevOps Team
