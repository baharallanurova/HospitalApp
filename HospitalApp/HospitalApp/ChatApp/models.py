from django.db import models
from django.utils import timezone
from hospital.models import User


class ChatMessage(models.Model):
    user_from = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    user_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    message = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_created']
        indexes = [
            models.Index(fields=['user_from', 'user_to']),
            models.Index(fields=['date_created']),
        ]

    def __str__(self):
        return f"{self.user_from} to {self.user_to}: {self.message[:20]}..."

    def mark_as_read(self):
        self.is_read = True
        self.save()