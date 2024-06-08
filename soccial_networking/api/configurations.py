from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


class CustomPagination(PageNumberPagination):
    page_size = 10


class FriendRequestThrottle(UserRateThrottle):
    rate = "3/minute"
