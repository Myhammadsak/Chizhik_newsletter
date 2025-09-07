# models.py
import json
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    telegram_api_id = models.CharField(max_length=10)
    telegram_api_hash = models.CharField(max_length=50)
    telegram_session_string = models.TextField(blank=True, null=True)
    is_telegram_authenticated = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Groups(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user_groups'
    )
    chats = models.JSONField(
        default=list,
        verbose_name='url of chats'
    )

    def __str__(self):
        return f"{self.user.username} - {self.chats}"

    def add_chats(self, new_links):
        current_chats = self.get_chats()
        added = 0

        for link in new_links:
            if link not in current_chats:
                current_chats.append(link)
                added += 1

        if added > 0:
            self.chats = current_chats
            self.save()
        return added

    def get_chats(self):
        if isinstance(self.chats, str):
            return json.loads(self.chats)
        return self.chats or []

    class Meta:
        verbose_name_plural = "Groups"


class Newsletter(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    file = models.FileField(blank=True, null=True)
    file2 = models.FileField(blank=True, null=True)
    file3 = models.FileField(blank=True, null=True)
    file4 = models.FileField(blank=True, null=True)
    file5 = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - content.{self.text}'