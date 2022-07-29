from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api import views

app_name = 'api'

router = SimpleRouter()
router.register('users', views.CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.SignUpUser.as_view(), name='signup'),
    path('v1/auth/token/', views.GetToken.as_view(), name='get_token'),
]
