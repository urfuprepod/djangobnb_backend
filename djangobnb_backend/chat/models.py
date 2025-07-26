from django.db import models
import uuid
from useraccount.models import User

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = ('Обращения')
# Create your models here.

class ConversationMessage(models.Model):
     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
     body = models.TimeField()
     sent_to = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
     created_by = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
     created_at = models.DateTimeField(auto_now_add=True)
     
     class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = ('Сообщения')