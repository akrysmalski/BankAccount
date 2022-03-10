"""BankAccount URL Configuration

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

from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers

from account.api.v1.views import AccountViewSet
from base.api.v1.views import UserViewSet



router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'api/v1/', include(router.urls))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
