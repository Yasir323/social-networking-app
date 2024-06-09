from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from .configurations import CustomPagination, FriendRequestThrottle
from .models import User, FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = []


class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email").lower()
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        # print(connection.queries)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "message": "Login Successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        keyword = self.request.query_params.get("q", "").lower()
        if "@" in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(username__icontains=keyword)


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [FriendRequestThrottle]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get("to_user_id")
        to_user = User.objects.get(id=to_user_id)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, status="pending"):
            return Response({"error": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)
        FriendRequest.objects.create(from_user=request.user, to_user=to_user, status="pending")
        return Response({"message": "Friend request sent"})


class ManageFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get("request_id")
        action = request.data.get("action")
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            if action == "accept":
                friend_request.status = "accepted"
            elif action == "reject":
                friend_request.status = "rejected"
            friend_request.save()
            return Response({"message": f"Friend request {action}ed"})
        except FriendRequest.DoesNotExist:
            return Response({"error": f"Friend request not found"}, status=status.HTTP_404_NOT_FOUND)


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            sent_requests__to_user=self.request.user,
            sent_requests__status="accepted"
        ) | User.objects.filter(
            received_requests__from_user=self.request.user,
            received_requests__status="accepted"
        )


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status="pending")
