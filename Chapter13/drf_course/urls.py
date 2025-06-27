from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .custom_token_view import CustomTokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    
    #http://127.0.0.1:8000/silk/
    path('silk/', include('silk.urls', namespace='silk')),
    
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
