# pagination.py (혹은 views.py 상단에 함께 작성 가능)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        current_page = (self.offset // self.limit) + 1 if self.limit else 1

        return Response({
            'total_count': self.count,                   # 전체 아이템 수
            'limit': self.limit,                   # 페이지당 개수
            'offset': self.offset,                 # 시작 오프셋
            'current_page': current_page,          # 현재 페이지 번호
            'next': self.get_next_link(),          # 다음 페이지 URL
            'previous': self.get_previous_link(),  # 이전 페이지 URL
            'results': data                        # 실제 데이터
        })
