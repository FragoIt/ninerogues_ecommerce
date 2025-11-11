from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError, NotFound

from apps.product.models import Product
from apps.product.serializers import ProductSerializer
from apps.category.models import Category

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class ProductDetailView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id = int(productId)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Optimización: select_related para cargar la categoría en una sola consulta
            product = Product.objects.select_related('category').get(id=product_id)
            product_serialized = ProductSerializer(product)
            return Response({'product': product_serialized.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product with this ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)


class ListProductsView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        # Validar y sanitizar parámetros
        sortBy = request.query_params.get('sortBy', 'date_created')
        ALLOWED_SORT_FIELDS = ['date_created', 'price', 'sold', 'name']
        
        if sortBy not in ALLOWED_SORT_FIELDS:
            sortBy = 'date_created'
        
        order = request.query_params.get('order')
        limit = request.query_params.get('limit', 6)

        try:
            limit = int(limit)
            if limit <= 0:
                limit = 6
        except (ValueError, TypeError):
            return Response(
                {'error': 'Limit must be a positive integer'},
                status=status.HTTP_400_BAD_REQUEST)
        
        # Aplicar orden
        if order == 'desc':
            sortBy = '-' + sortBy
        
        # Optimización: select_related para cargar categorías en una sola consulta
        products_query = Product.objects.select_related('category').order_by(sortBy)
        
        if limit:
            products_query = products_query[:limit]

        products = ProductSerializer(products_query, many=True)

        return Response({'products': products.data}, status=status.HTTP_200_OK)


class ListSearchView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        try:
            category_id = int(data.get('category_id', 0))
        except (ValueError, TypeError):
            return Response(
                {'error': 'Category ID must be an integer'},
                status=status.HTTP_400_BAD_REQUEST)

        search = data.get('search', '').strip()

        # Optimización: Iniciar con select_related
        search_results = Product.objects.select_related('category')

        # Aplicar búsqueda si hay texto
        if search:
            # TODO: Para mejor rendimiento, considerar implementar búsqueda full-text de PostgreSQL
            search_results = search_results.filter(
                Q(description__icontains=search) | Q(name__icontains=search)
            )

        # Filtrar por categoría si se especifica
        if category_id != 0:
            try:
                category = Category.objects.prefetch_related('category_set').get(id=category_id)
                
                # Determinar categorías a filtrar
                if category.parent:
                    categories_to_filter = [category]
                else:
                    child_categories = list(category.category_set.all())
                    categories_to_filter = [category] + child_categories
                
                search_results = search_results.filter(category__in=categories_to_filter)
            except Category.DoesNotExist:
                return Response(
                    {'error': 'Category not found'},
                    status=status.HTTP_404_NOT_FOUND)
        
        # Ordenar y serializar
        search_results = search_results.order_by('-date_created')
        serialized_results = ProductSerializer(search_results, many=True)
        
        return Response({'search_products': serialized_results.data}, status=status.HTTP_200_OK)


class ListRelatedView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, productId, format=None):
        try:
            product_id = int(productId)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Product ID must be an integer'},
                status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Optimización: select_related para obtener la categoría en una sola consulta
            product = Product.objects.select_related('category').get(id=product_id)
            category = product.category
        except Product.DoesNotExist:
            return Response(
                {'error': 'Product with this product ID does not exist'},
                status=status.HTTP_404_NOT_FOUND)
        
        # Determinar categorías a filtrar
        if category.parent:
            # Si la categoría tiene padre, filtrar solo por esta categoría
            categories_to_filter = [category]
        else:
            # Si es categoría padre, incluir todas las subcategorías
            child_categories = list(Category.objects.filter(parent=category))
            categories_to_filter = [category] + child_categories
        
        # Optimización: Una sola consulta con select_related
        related_products = (Product.objects
                           .select_related('category')
                           .filter(category__in=categories_to_filter)
                           .exclude(id=product_id)
                           .order_by('-sold')[:3])  # Limitar a 3 desde la BD
        
        if related_products.exists():
            serialized_products = ProductSerializer(related_products, many=True)
            return Response(
                {'related_products': serialized_products.data},
                status=status.HTTP_200_OK)
        else:
            return Response(
                {'related_products': []},
                status=status.HTTP_200_OK)


class ListBySearchView(APIView):
    permission_classes = (permissions.AllowAny, )

    # Constantes para mejor mantenibilidad
    PRICE_RANGES = {
        '1 - 19': (1, 20),
        '20 - 39': (20, 40),
        '40 - 59': (40, 60),
        '60 - 79': (60, 80),
        'More than 80': (80, None)
    }
    ALLOWED_SORT_FIELDS = ['date_created', 'price', 'sold', 'name']

    def post(self, request, format=None):
        data = self.request.data

        try:
            category_id = int(data.get('category_id', 0))
        except (ValueError, TypeError):
            return Response(
                {'error': 'Category ID must be an integer'},
                status=status.HTTP_400_BAD_REQUEST)
        
        price_range = data.get('price_range', '')
        sort_by = data.get('sort_by', 'date_created')
        order = data.get('order', 'asc')

        # Validar sort_by
        if sort_by not in self.ALLOWED_SORT_FIELDS:
            sort_by = 'date_created'

        # Filtrar por categoría
        if category_id == 0:
            product_results = Product.objects.select_related('category').all()
        else:
            try:
                category = Category.objects.prefetch_related('category_set').get(id=category_id)
                
                # Determinar categorías a filtrar
                if category.parent:
                    categories_to_filter = [category]
                else:
                    child_categories = list(category.category_set.all())
                    categories_to_filter = [category] + child_categories
                
                product_results = Product.objects.select_related('category').filter(
                    category__in=categories_to_filter)
            except Category.DoesNotExist:
                return Response(
                    {'error': 'This category does not exist'},
                    status=status.HTTP_404_NOT_FOUND)

        # Filtrar por rango de precio
        if price_range in self.PRICE_RANGES:
            min_price, max_price = self.PRICE_RANGES[price_range]
            product_results = product_results.filter(price__gte=min_price)
            if max_price is not None:
                product_results = product_results.filter(price__lt=max_price)
        
        # Aplicar ordenamiento
        if order == 'desc':
            sort_by = '-' + sort_by
        
        product_results = product_results.order_by(sort_by)
        
        # Serializar resultados
        serialized_products = ProductSerializer(product_results, many=True)

        return Response(
            {'filtered_products': serialized_products.data},
            status=status.HTTP_200_OK)