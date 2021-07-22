from django.core.checks import messages
from django.http import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserDetailSerializer
from rest_framework.decorators import action
from .permissions import UserDetailedAuthOnly


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (UserDetailedAuthOnly,)

    @action(methods=('get', 'patch'), detail=False)
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'GET':
            serializer = UserDetailSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserDetailSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
