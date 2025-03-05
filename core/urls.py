from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

# Create a router for viewsets
router = DefaultRouter()

app_name = 'core'

# Web routes (HTML responses)
web_patterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns = [
    *web_patterns,
    
    # API routes (JSON responses) for DRF
    path('api/', include([
        # Router-generated resource endpoints
        *router.urls,
        # Manual resource endpoints
        path('users/', views.UserListAPIView.as_view(), name='user-list'),
    ])),
]