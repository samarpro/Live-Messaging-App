from django.db import models
from ChatAuth.models import CustomAbstractUser
# Create your models here.


class ChatsModel(models.Model):
    sender = models.ForeignKey(CustomAbstractUser,on_delete=models.CASCADE, related_name = "sent_chats")
    receiver = models.ForeignKey(CustomAbstractUser, on_delete = models.CASCADE, related_name = "received_chats")
    message = models.TextField(default=None)
    GroupName = models.TextField(default =None)
    timeStamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.sender.first_name} sent to {self.receiver.first_name}   --- {self.timeStamp}"
        
    