from core.response import APIResponse
from users.models.UserProfile import UserProfile
from users.serializers.UserProfileSerializer import UserProfileSerializer
from rest_framework import permissions, status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description="Get user profile",
        responses={200: UserProfileSerializer}
    ),
    create=extend_schema(
        description="Create user profile",
        request=UserProfileSerializer,
        responses={201: UserProfileSerializer}
    ),
    update=extend_schema(
        description="Update user profile",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer}
    ),
    partial_update=extend_schema(
        description="Partially update user profile",
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer}
    )
)
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj, created = UserProfile.objects.get_or_create(
            user=self.request.user,
            defaults={
                'full_name': '',
                'age': 0,
                'discovery_source': 'google',
                'stem_level': 'beginner',
                'daily_goal': 5
            }
        )
        return obj

    def list(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        # If profile already exists, update it
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile, data=request.data)
        except UserProfile.DoesNotExist:
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return APIResponse(data=serializer.data, code=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()