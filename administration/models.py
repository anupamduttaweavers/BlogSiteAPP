from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
import random
from datetime import timedelta


class Account(models.Model):
    fullname = models.CharField(max_length=250, verbose_name="Full Name")
    username = models.CharField(max_length=150, unique=True, verbose_name="Username")
    password = models.CharField(max_length=128, verbose_name="Password")  # Store hashed passwords
    email = models.EmailField(max_length=254, unique=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="Phone Number")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Account Created At")

    def save(self, *args, **kwargs):
        # Hash the password before saving if it's not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Session(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="session")
    session_key = models.CharField(max_length=255, unique=True, verbose_name="Session Key")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Session Created At")
    expires_at = models.DateTimeField(verbose_name="Session Expires At")

    def is_valid(self):
        """Check if the session is still valid."""
        return now() < self.expires_at

    def __str__(self):
        return f"Session for {self.user.username}"


class OTP(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, verbose_name="OTP Code")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="OTP Created At")
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified")

    def generate_otp(self):
        """Generate a random 6-digit OTP."""
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.created_at = now()
        self.save()

    def is_expired(self, expiry_minutes=5):
        """Check if the OTP has expired."""
        expiry_time = self.created_at + timedelta(minutes=expiry_minutes)
        return now() > expiry_time

    def __str__(self):
        return f"OTP for {self.user.username}: {self.otp_code} (Verified: {self.is_verified})"
