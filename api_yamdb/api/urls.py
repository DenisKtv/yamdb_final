from api.views.reviews import (CategoryViewSet, CommentViewSet, GenreViewSet,
                               ReviewViewSet, TitleViewSet)
from api.views.users import UserViewSet, emailcheck, signup
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='auth_signup'),
    path('v1/auth/token/', emailcheck, name='auth_token'),
]
