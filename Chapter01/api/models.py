import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# 사용자 모델: Django의 기본 사용자 모델을 확장한 커스텀 유저
class User(AbstractUser):
    pass

# 상품 모델: 상품 정보를 저장
class Product(models.Model):
    # 상품명
    name = models.CharField(max_length=200)  
     # 상품 설명
    description = models.TextField()   
     # 가격 (소수점 2자리까지 허용)     
    price = models.DecimalField(max_digits=10, decimal_places=2) 
     # 재고 수량 (양의 정수만 가능)
    stock = models.PositiveIntegerField()   
     # 상품 이미지
    image = models.ImageField(upload_to='products/', blank=True, null=True) 


    #@property는 Python의 내장 데코레이터로, 클래스의 메서드를 마치 속성로 만들어주는 문법
    @property  
    def in_stock(self):
        return self.stock > 0  # 재고가 0보다 크면 True 반환

    def __str__(self):
        return self.name  # 관리자 페이지 등에서 객체 이름으로 표시됨


# 주문 모델
class Order(models.Model):
    # 주문 상태를 선택할 수 있도록 Enum 형식으로 구성
    class StatusChoices(models.TextChoices):
        PENDING = 'Pending'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'

    # UUID를 기본키로 사용
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)  
    # 주문한 사용자
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    #주문 생성 시각
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING  # 기본값은 PENDING
    )

    # 주문-상품 다대다 관계 설정 (중간 모델 OrderItem 사용)
    products = models.ManyToManyField(Product, through="OrderItem", related_name='orders')
    
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


# 주문 상세 항목 모델 (중간 테이블)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField() 

    # 해당 항목의 소계 계산
    @property
    def item_subtotal(self):
        return self.product.price * self.quantity  

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"
