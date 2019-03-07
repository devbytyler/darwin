from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [ 
    path('', include('darwin.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]
