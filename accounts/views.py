from django.shortcuts import render
from rest_framework import viewsets
from .models import User, GovernmentOrganization
from .serializers import UserSerializer, GovernmentOrganizationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class UsersMeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

from rest_framework.permissions import BasePermission

class IsAdminOrReadOnlyForOrg(BasePermission):
    """
    Custom permission: Only users with role 'admin' can create organizations.
    Users with role 'gov_org' can only view their associated organization.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for gov_org users only for their org
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            if getattr(request.user, 'role', None) == 'gov_org':
                return obj == getattr(request.user, 'organization', None)
            return True
        # Only admin can modify
        return getattr(request.user, 'role', None) == 'admin'

class GovernmentOrganizationViewSet(viewsets.ModelViewSet):
    queryset = GovernmentOrganization.objects.all()
    serializer_class = GovernmentOrganizationSerializer
    permission_classes = [IsAdminOrReadOnlyForOrg]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and getattr(user, 'role', None) == 'gov_org':
            # Only show the organization the gov_org user is associated with
            if user.organization:
                return GovernmentOrganization.objects.filter(id=user.organization.id)
            return GovernmentOrganization.objects.none()
        return GovernmentOrganization.objects.all()