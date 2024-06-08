from django.urls import path
from soccial_networking.api.views import (
    SignupView,
    LoginView,
    UserSearchView,
    SendFriendRequestView,
    ManageFriendRequestView,
    ListFriendsView,
    ListPendingRequestsView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("search/", UserSearchView.as_view(), name="user-search"),
    path("friend-request/send/", SendFriendRequestView.as_view(), name="send-friend-request"),
    path("friend-request/manage/", ManageFriendRequestView.as_view(), name="manage-friend-request"),
    path("friends/", ListFriendsView.as_view(), name="list-friends"),
    path("friend-request/pending/", ListPendingRequestsView.as_view(), name="list-pending-friend-request"),
]
