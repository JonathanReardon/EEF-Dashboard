from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    # ... other URL patterns ...
    path('upload-json/', views.upload_json, name='upload_json'),
]