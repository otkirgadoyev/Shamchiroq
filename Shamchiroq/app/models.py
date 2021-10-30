from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=12, unique=True)
    gender = models.CharField(max_length=100, choices=GENDERS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card_number = models.CharField(max_length=16)
    voice = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class Voice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Voice')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Subscription')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField(auto_created=True, editable=True)
    is_active = models.BooleanField(default=False)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Payment')
    price = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Verify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Verify')
    phone_number = models.CharField(max_length=12, unique=True)
    verify_code = models.CharField(max_length=6, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Audio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Audio')
    text = models.TextField()
    link = models.CharField(max_length=200)
    is_file = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
