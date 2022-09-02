from django.urls import include, path
from rest_framework.routers import SimpleRouter
from api import views

app_name = 'api'

router = SimpleRouter()
router.register('users', views.CustomUserViewSet, basename='users')
router.register('categories', views.CategoryViewSet, basename='сategories')
router.register('titles', views.TitleViewSet, basename='titles')
router.register('genres', views.GenreViewSet, basename='genres')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', views.SignUpUser.as_view(), name='signup'),
    path('v1/auth/token/', views.GetToken.as_view(), name='get_token'),
]
