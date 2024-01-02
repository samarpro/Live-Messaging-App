from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomAbstractUser(AbstractUser):

    # overwriting save() method declared in AbstractUser->AbstractBaseUser->models.Model
    def save(self,*args,**kwargs):
        self.last_login = timezone.now()
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.first_name