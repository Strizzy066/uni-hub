from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import search_communities


# Create a router for viewsets
router = DefaultRouter()

app_name = 'core'

# Web routes (HTML responses)
web_patterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'), 
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
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

urlpatterns += [
    path('search/', search_communities, name='search_communities'),
]
