"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="Tabriknoma API",
      default_version='v1',
      description="API for Tabriknoma",
      terms_of_service="https://www.tabriknoma.uz/policies/terms/",
      contact=openapi.Contact(email="contact@tabriknoma.uz"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("api/v1/", include("dj_rest_auth")),
    path('api/v1/wish/', include('wish.urls')),
    path('api/v1/otp/', include('otp.urls')),
    path('payme/', include('my_payme.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='tabriknoma project'),
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from rest_framework_simplejwt.views import TokenVerifyView

from dj_rest_auth.jwt_auth import get_refresh_view

urlpatterns += [
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
]