from django.contrib import admin
from django.urls import path, include
from home import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'auth', views.AuthViewSet, basename="auth")

urlpatterns = [
    path('', include(router.urls)),  # Use the router's URLs
    path('admin/', admin.site.urls),
]