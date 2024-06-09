from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):

    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # groups = models.ManyToManyField(
    #     Group,
    #     related_name='custom_user_set',  # Changed related name
    #     blank=True,
    #     help_text=(
    #         'The groups this user belongs to. A user will get all permissions '
    #         'granted to each of their groups.'
    #     ),
    #     verbose_name='groups',
    # )
    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name='custom_user_set',  # Changed related name
    #     blank=True,
    #     help_text='Specific permissions for this user.',
    #     verbose_name='user permissions',
    # )

    def __str__(self):
        return self.email


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected")
    )
    from_user = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.status})"
