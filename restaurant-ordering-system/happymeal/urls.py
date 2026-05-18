"""
URL configuration for happymeal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path
from restaurants.auth_views import RateLimitedAuthTokenView, RateLimitedTokenObtainPairView
from restaurants.forms import EmailOrUsernameAuthenticationForm
from restaurants import views as restaurant_views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', include('restaurants.urls')),
    path('', include('orders.urls')),
    path('api/auth-token/', RateLimitedAuthTokenView.as_view(), name='api_auth_token'),
    path('api/token/', RateLimitedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'accounts/login/',
        LoginView.as_view(
            authentication_form=EmailOrUsernameAuthenticationForm,
            template_name='registration/login.html',
        ),
        name='login',
    ),
    path(
        'accounts/logout/',
        LogoutView.as_view(next_page='home'),
        name='logout',
    ),
    path('accounts/register/', restaurant_views.register, name='register'),
    path(
        'accounts/password-reset/',
        PasswordResetView.as_view(
            email_template_name='registration/account_password_reset_email.html',
            subject_template_name='registration/account_password_reset_subject.txt',
            template_name='registration/account_password_reset_form.html',
            success_url='/accounts/password-reset/done/',
        ),
        name='password_reset',
    ),
    path(
        'accounts/password-reset/done/',
        PasswordResetDoneView.as_view(template_name='registration/account_password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'accounts/reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='registration/account_password_reset_confirm.html',
            success_url='/accounts/reset/done/',
        ),
        name='password_reset_confirm',
    ),
    path(
        'accounts/reset/done/',
        PasswordResetCompleteView.as_view(template_name='registration/account_password_reset_complete.html'),
        name='password_reset_complete',
    ),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = restaurant_views.custom_404
