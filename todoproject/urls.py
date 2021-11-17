"""todoproject URL Configuration

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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from rest_framework import routers
from todos.views import TodoViewSet, LoginView
from rest_framework_simplejwt import views as jwt_views


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# serializers.py
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token

# views.py
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# create a new router
router = routers.DefaultRouter()
# register our viewsets
router.register(r'todos', TodoViewSet)  #register "/todos" routes

urlpatterns = [
    # add all of our router urls
    path('', include(router.urls)),
    path('api/token/',
         MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/',
         jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
    path('user/login/', LoginView.as_view(), name="auth-login"),
    path('admin/', admin.site.urls),
    re_path('(^(?!(api|admin)).*$)',
            TemplateView.as_view(template_name='index.html'))
]
