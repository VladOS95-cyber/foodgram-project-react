from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from receipt.all_serializers import FollowSerializer, UserDetailSerializer

from .models import CustomUser, Follow
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


class SubscribeView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        if Follow.objects.filter(user=user, following=author).exists():
            return Response(
                'Вы уже подписаны',
                status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(user=user, following=author)
        serializer = UserDetailSerializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        follow = Follow.objects.get(user=user, following=author)
        follow.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class ShowSubscriptionsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        following = Follow.objects.filter(user=user).all()
        serializer = FollowSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
