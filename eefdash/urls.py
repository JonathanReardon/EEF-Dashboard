from django.contrib import admin
from django.urls import path, include
from myapp import urls as myapp_urls  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myapp/', include((myapp_urls, 'myapp'))),
]
