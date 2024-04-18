from django.db import models
from core.models import TimeStampMixin
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from .constants import GENDER_TYPE, BLOOD_TYPE
# Create your models here.
class User(TimeStampMixin, AbstractUser):
    image = models.ImageField(upload_to='account/images/')
    phone = models.CharField(max_length=15)
    balance = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    email = models.EmailField(unique=True)
    address = models.TextField()
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=10)
    total_donated = models.IntegerField(default=0)
    last_donation_date = models.DateField(null=True, blank=True, default=None)
    is_available = models.BooleanField(default=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self) -> str:
        return f"{self.username}"
    


class OneTimePassword(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"
