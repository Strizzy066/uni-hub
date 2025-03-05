from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm

# DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import UserSerializer
from .models import User

# Create your views here.
def home(request):
    """
    View function for the home page of the site.
    """
    return render(request, 'core/home.html')

# Web views (HTML templates)
def register_view(request):
    """
    Web view function for user registration.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to Uni Hub.")
            return redirect('core:home')
        else:
            for error in form.errors.values():
                messages.error(request, error[0])
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/registration.html', {'form': form})

def login_view(request):
    """
    Web view function for user login.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                messages.success(request, f"Welcome back, {user.first_name if user.first_name else user.email}!")
                return redirect('core:home')
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    Web view function for user logout.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('core:home')

# API Views
class UserListAPIView(APIView):
    """
    API view to retrieve a list of all registered users.
    Only accessible to admin users for security reasons.
    """
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        """
        Get a list of all users with their details.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        
        # Get count of users
        user_count = users.count()
        
        # Return user data along with additional information
        response_data = {
            'count': user_count,
            'users': serializer.data,
            'admin_count': User.objects.filter(is_staff=True).count(),
        }
        
        return Response(response_data, status=status.HTTP_200_OK)