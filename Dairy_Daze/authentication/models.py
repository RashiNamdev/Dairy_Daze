from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.hashers import make_password
import random

# Custom User Model
class CustomUser(models.Model):
    email = models.EmailField(unique=True, db_index=True)  # Index for faster queries
    password = models.CharField(max_length=128)  # Will store hashed password
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_"):
            self.password = make_password(self.password)  # Hash password before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
def now_plus_5():
    return now() + timedelta(minutes=5)

# OTP Model
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  # OTP linked to user
    email =  models.EmailField(unique=True, default="test@example.com")
    otp_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=now_plus_5)  # OTP expires in 5 min

    @staticmethod
    def generate_otp():
        return random.randint(100000, 999999)  # 6-digit OTP

    def is_expired(self):
        return now() > self.expires_at  # Check if OTP expired

    def __str__(self):
        return f"OTP for {self.user.email}: {self.otp_code}"

    @staticmethod
    def cleanup_expired_otps():
        OTP.objects.filter(expires_at__lt=now()).delete()  # Delete expired OTPs
