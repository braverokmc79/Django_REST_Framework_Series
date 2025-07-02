from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models import Product
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    제품이 생성, 업데이트 또는 삭제될 때 제품 목록 캐시를 무효화합니다.
    """
    print("제품 캐시 지우기")
    
    # Clear product list caches
    cache.delete_pattern('*product_list*')