# Guía de Contribución - NineRogues E-Commerce

¡Gracias por tu interés en contribuir a NineRogues E-Commerce! Este documento proporciona las pautas y el proceso para contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Features](#sugerir-features)

---

## 📜 Código de Conducta

### Nuestro Compromiso

Nos comprometemos a hacer de la participación en este proyecto una experiencia libre de acoso para todos, independientemente de edad, tamaño corporal, discapacidad, etnia, identidad de género, nivel de experiencia, nacionalidad, apariencia personal, raza, religión o identidad y orientación sexual.

### Comportamiento Esperado

- Usar lenguaje acogedor e inclusivo
- Respetar puntos de vista y experiencias diferentes
- Aceptar críticas constructivas con gracia
- Enfocarse en lo que es mejor para la comunidad
- Mostrar empatía hacia otros miembros

### Comportamiento Inaceptable

- Lenguaje o imágenes sexualizadas
- Trolling, comentarios insultantes/despectivos
- Acoso público o privado
- Publicar información privada de otros sin permiso
- Conducta que podría considerarse inapropiada en un entorno profesional

---

## 🤝 Cómo Contribuir

### Tipos de Contribuciones Bienvenidas

1. **Reportar Bugs** 🐛
2. **Sugerir Features** 💡
3. **Mejorar Documentación** 📚
4. **Escribir Tests** ✅
5. **Arreglar Bugs** 🔧
6. **Implementar Features** ✨
7. **Mejorar Performance** ⚡
8. **Refactoring** 🔨

### Primeros Pasos

1. **Fork** el repositorio
2. **Clone** tu fork localmente
3. **Crea** una rama para tu feature/fix
4. **Desarrolla** tu contribución
5. **Push** a tu fork
6. **Crea** un Pull Request

---

## 🔄 Proceso de Desarrollo

### 1. Setup del Entorno

Sigue la [Guía de Instalación](INSTALLATION.md) para configurar tu entorno de desarrollo.

### 2. Crear una Rama

```bash
# Actualizar main
git checkout main
git pull origin main

# Crear rama con nombre descriptivo
git checkout -b feature/nombre-descriptivo
# o
git checkout -b fix/nombre-del-bug
```

**Convenciones de nombres de ramas:**
- `feature/` - Nueva funcionalidad
- `fix/` - Corrección de bug
- `docs/` - Cambios en documentación
- `refactor/` - Refactorización de código
- `test/` - Añadir o modificar tests
- `style/` - Cambios de formato/estilo

### 3. Desarrollar tu Contribución

**Mejores Prácticas:**
- Haz commits pequeños y atómicos
- Escribe tests para nueva funcionalidad
- Actualiza documentación si es necesario
- Sigue los estándares de código
- Ejecuta tests antes de hacer push

### 4. Testing

```bash
# Backend (Django)
python manage.py test

# Frontend (React)
npm test

# Linting
flake8 apps/
npm run lint  # Si está configurado
```

### 5. Commit y Push

```bash
git add .
git commit -m "tipo: descripción corta"
git push origin nombre-de-tu-rama
```

### 6. Crear Pull Request

1. Ve a GitHub y crea un PR desde tu rama
2. Llena el template de PR completamente
3. Espera revisión y feedback
4. Realiza cambios si son solicitados
5. Una vez aprobado, será merged

---

## 💻 Estándares de Código

### Python (Backend)

#### Style Guide

Seguimos [PEP 8](https://www.python.org/dev/peps/pep-0008/) con algunas excepciones:

- **Longitud de línea:** 100 caracteres (no 79)
- **Imports:** Organizados en orden alfabético dentro de cada grupo
- **Docstrings:** Usar formato Google

#### Ejemplo de Código Bien Formateado

```python
"""
Module docstring describing what this module does.
"""
from django.db import models
from django.contrib.auth import get_user_model

from apps.product.models import Product

User = get_user_model()


class Order(models.Model):
    """
    Representa una orden de compra.
    
    Attributes:
        user: Usuario que realizó la orden
        status: Estado actual de la orden
        total: Monto total de la orden
    """
    
    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Orden'
        verbose_name_plural = 'Órdenes'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text='Usuario que realizó la orden'
    )
    status = models.CharField(max_length=50, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.email}"
    
    def calculate_total(self):
        """
        Calcula el total de la orden sumando todos los items.
        
        Returns:
            Decimal: Total de la orden
        """
        return sum(item.subtotal for item in self.items.all())
```

#### Linting y Formatting

```bash
# Instalar herramientas
pip install flake8 black isort

# Ejecutar
flake8 apps/
black apps/
isort apps/
```

**Configuración en `setup.cfg`:**

```ini
[flake8]
max-line-length = 100
exclude = migrations,venv,build,dist
ignore = E203,W503

[isort]
profile = black
line_length = 100
```

### JavaScript/React (Frontend)

#### Style Guide

Seguimos [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

#### Ejemplo de Componente React

```javascript
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { useDispatch, useSelector } from 'react-redux';
import { getProducts } from '../redux/actions/products';

/**
 * Componente que muestra la lista de productos
 * 
 * @param {Object} props - Props del componente
 * @param {string} props.category - Categoría a filtrar
 * @returns {JSX.Element} Lista de productos
 */
const ProductList = ({ category }) => {
  const dispatch = useDispatch();
  const { products, loading } = useSelector(state => state.products);
  const [filteredProducts, setFilteredProducts] = useState([]);

  useEffect(() => {
    dispatch(getProducts());
  }, [dispatch]);

  useEffect(() => {
    if (category) {
      setFilteredProducts(
        products.filter(product => product.category === category)
      );
    } else {
      setFilteredProducts(products);
    }
  }, [category, products]);

  if (loading) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="product-list">
      {filteredProducts.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
};

ProductList.propTypes = {
  category: PropTypes.string,
};

ProductList.defaultProps = {
  category: null,
};

export default ProductList;
```

#### ESLint

```bash
# Ejecutar linting
npm run lint

# Fix automático
npm run lint:fix
```

---

## 📝 Commit Messages

### Formato

```
tipo(scope): descripción corta

Descripción más detallada si es necesario.

Fixes #123
```

### Tipos

- `feat` - Nueva funcionalidad
- `fix` - Corrección de bug
- `docs` - Cambios en documentación
- `style` - Formato, punto y coma, etc (no cambios de código)
- `refactor` - Refactorización
- `test` - Añadir tests
- `chore` - Mantenimiento, configuración
- `perf` - Mejora de performance

### Ejemplos

```bash
feat(cart): añadir funcionalidad de guardar para después

Permite a los usuarios guardar items del carrito para comprar después.
Incluye nuevo modelo SavedItem y endpoints de API.

Fixes #45

---

fix(payment): corregir cálculo de impuestos

El impuesto se estaba calculando dos veces en checkout.
Ahora se calcula correctamente una sola vez.

Fixes #123

---

docs(readme): actualizar sección de instalación

Añadida información sobre configuración de PostgreSQL.

---

refactor(auth): simplificar lógica de login

Removed código duplicado y mejorada legibilidad.
Sin cambios funcionales.
```

---

## 🔀 Pull Requests

### Template de PR

Cuando crees un PR, incluye:

```markdown
## Descripción
Breve descripción de los cambios realizados.

## Tipo de Cambio
- [ ] Bug fix (non-breaking change)
- [ ] Nueva feature (non-breaking change)
- [ ] Breaking change (fix o feature que causa que funcionalidad existente no funcione como se esperaba)
- [ ] Documentación

## Cómo se ha Testeado?
Describe los tests que ejecutaste para verificar tus cambios.

## Checklist
- [ ] Mi código sigue los estándares del proyecto
- [ ] He realizado self-review de mi código
- [ ] He comentado mi código, especialmente en áreas difíciles
- [ ] He actualizado la documentación correspondiente
- [ ] Mis cambios no generan nuevos warnings
- [ ] He añadido tests que prueban que mi fix/feature funciona
- [ ] Tests nuevos y existentes pasan localmente
- [ ] Cambios dependientes han sido merged

## Screenshots (si aplica)
Añade screenshots para demostrar cambios visuales.

## Issues Relacionados
Fixes #123
Related to #456
```

### Proceso de Revisión

1. **Automated Checks** - CI/CD ejecuta tests automáticamente
2. **Code Review** - Al menos 1 aprobación requerida
3. **Testing** - Reviewer prueba los cambios
4. **Discussion** - Se discuten cambios si es necesario
5. **Approval** - PR es aprobado
6. **Merge** - PR es merged a main

### Tips para PRs Exitosos

- ✅ **Pequeños y enfocados** - Un PR debería hacer una cosa
- ✅ **Bien descritos** - Explica qué y por qué
- ✅ **Tests incluidos** - Nuevo código debe tener tests
- ✅ **Sin conflictos** - Resuelve conflictos antes de solicitar review
- ✅ **Documentación actualizada** - Si cambias funcionalidad
- ❌ **No mezcles concerns** - No combines múltiples features

---

## 🐛 Reportar Bugs

### Antes de Reportar

1. **Busca** en issues existentes
2. **Verifica** en la última versión
3. **Determina** si es realmente un bug

### Template de Bug Report

```markdown
## Descripción del Bug
Descripción clara y concisa del bug.

## Pasos para Reproducir
1. Ve a '...'
2. Click en '...'
3. Scroll hasta '...'
4. Ver error

## Comportamiento Esperado
Qué esperabas que sucediera.

## Comportamiento Actual
Qué sucedió realmente.

## Screenshots
Si aplica, añade screenshots.

## Entorno
- OS: [e.g., macOS 12.0]
- Browser: [e.g., Chrome 95]
- Django Version: [e.g., 3.1.7]
- React Version: [e.g., 17.0.2]

## Información Adicional
Cualquier otro contexto sobre el problema.

## Logs
```
Pega logs relevantes aquí
```
```

---

## 💡 Sugerir Features

### Template de Feature Request

```markdown
## Feature Request

### Problema que Resuelve
Descripción clara del problema o necesidad.

### Solución Propuesta
Descripción clara de lo que quieres que suceda.

### Alternativas Consideradas
Otras soluciones que consideraste.

### Información Adicional
Contexto adicional, screenshots, mockups.

### ¿Estás dispuesto a contribuir?
- [ ] Sí, puedo trabajar en esto
- [ ] Necesitaría ayuda
- [ ] Solo sugiriendo
```

---

## ✅ Testing

### Backend Testing

```python
# apps/cart/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.cart.models import Cart, CartItem
from apps.product.models import Product

User = get_user_model()


class CartModelTest(TestCase):
    """Tests para el modelo Cart"""
    
    def setUp(self):
        """Setup ejecutado antes de cada test"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.cart = Cart.objects.create(user=self.user)
    
    def test_cart_creation(self):
        """Test de creación de carrito"""
        self.assertEqual(self.cart.user, self.user)
        self.assertEqual(self.cart.total_items, 0)
    
    def test_add_item_to_cart(self):
        """Test de añadir item al carrito"""
        # Implementar test
        pass
```

### Frontend Testing

```javascript
// src/components/ProductCard.test.js
import { render, screen } from '@testing-library/react';
import ProductCard from './ProductCard';

describe('ProductCard', () => {
  const mockProduct = {
    id: 1,
    name: 'Test Product',
    price: 99.99,
    image: 'test.jpg'
  };

  test('renders product name', () => {
    render(<ProductCard product={mockProduct} />);
    const nameElement = screen.getByText(/Test Product/i);
    expect(nameElement).toBeInTheDocument();
  });

  test('renders product price', () => {
    render(<ProductCard product={mockProduct} />);
    const priceElement = screen.getByText(/99.99/i);
    expect(priceElement).toBeInTheDocument();
  });
});
```

---

## 📚 Recursos

### Documentación
- [Django Docs](https://docs.djangoproject.com/)
- [React Docs](https://react.dev/)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows)

### Tutoriales
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/)
- [Pull Request Best Practices](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)

---

## 🙏 Agradecimientos

¡Gracias por contribuir a NineRogues E-Commerce! Cada contribución, por pequeña que sea, es valiosa y apreciada.

---

**Questions?** Abre un issue con la etiqueta `question` o contacta al equipo.

**Happy Coding! 🚀**
