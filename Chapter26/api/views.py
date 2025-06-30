from django.db.models import Max
from api.serializers import OrderSerializer, ProductInfoSerializer, ProductSerializer,OrderCreateSerializer ,UserSerializer
from api.models import Product, Order, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import (IsAuthenticated,IsAdminUser,AllowAny)
from api.filters import ProductFilter , InStockFilterBackend , OrderFilter
from rest_framework import generics ,filters , viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.decorators import action

from drf_course.custom_pagination import CustomLimitOffsetPagination

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

#🔖 mixin_generics 형태
## POST 요청을 이용한 데이터 생성 : CreateAPIVIew

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        InStockFilterBackend
    ]
    search_fields = ['=name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = None

    @method_decorator(cache_page(60 * 15, key_prefix='product_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        import time
        time.sleep(2)
        return super().get_queryset()    
        
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()



   
   
   
   
   



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = None
#     filterset_class = OrderFilter
#     filter_backends = [DjangoFilterBackend]
    
#     @action(
#         detail=False,             # 여러 개를 다루는 list 형식 (단일 객체 X)
#         methods=['get'],          # GET 요청만 허용
#         url_path='user-orders',   # URL: `/orders/user-orders/` 로 접근
#     )
#     def user_orders(self, request):
#         filtered_qs = self.filter_queryset(self.get_queryset())  # 필터셋, 검색, 정렬 적용됨
#         orders = filtered_qs.filter(user=request.user)  # 여기에 사용자 필터 추가
#         serializer = self.get_serializer(orders, many=True)     # 여러 개니까 many=True
#         return Response(serializer.data)                        # 직렬화된 JSON 응답 반환


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # can also check if POST: if self.request.method == 'POST'
        if self.action in ['create', 'update']:
            return OrderCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


# class OrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer


# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         qs =super().get_queryset()
#         return qs.filter(user=self.request.user)
    
       

class ProductInfoAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': products.count(),
            'max_price': products.aggregate(max_price=Max('price'))['max_price']
        })
        return Response(serializer.data)



class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = None



