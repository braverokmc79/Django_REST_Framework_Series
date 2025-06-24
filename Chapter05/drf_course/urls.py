from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    
    #http://127.0.0.1:8000/silk/
    path('silk/', include('silk.urls', namespace='silk')),
]
