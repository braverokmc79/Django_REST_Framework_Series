from django.db.models import Max
from django.shortcuts import get_object_or_404
from api.serializers import ProductInfoSerializer, ProductSerializer, OrderSerializer
from api.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

from api.models import Product, Order, OrderItem



@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def product_info(request):
    proudcts =Product.objects.all()
    serializer = ProductInfoSerializer({
        'products':proudcts,
        'count':len(proudcts),
        'max_price':proudcts.aggregate(max_price=Max('price'))['max_price']
    })
    return Response(serializer.data)









