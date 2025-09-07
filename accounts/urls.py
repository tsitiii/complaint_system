from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UsersMeView, GovernmentOrganizationViewSet
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'organizations', GovernmentOrganizationViewSet, basename='organizations')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/users/me/',UsersMeView.as_view(), name='me/'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]