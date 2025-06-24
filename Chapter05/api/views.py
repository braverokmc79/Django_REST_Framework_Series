from django.db.models import Max
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer
from api.models import Product, Order, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer =ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):    
    orders = Order.objects.prefetch_related('items__product')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': products.count(),
        'max_price': products.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)