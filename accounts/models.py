from django.db import models
from django.contrib.auth.models import User

class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.user.username