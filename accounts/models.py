from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.manager import CustomeUserManager
import uuid

# Create your models here.
class User(AbstractUser):
    username = None
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    date_of_birth = models.DateField(_("date of birth"), max_length=150, blank=False)
    verified = models.BooleanField(_("verified"), default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomeUserManager()

    def __str__(self):
        return self.email


