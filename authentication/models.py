from django.db import models
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager
    )
from django.utils.translation import ugettext_lazy as _

# USER = get_user_model()

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_app_client = models.BooleanField(null=True, blank=True)
    is_app_staff = models.BooleanField(null=True, blank=True)
    is_app_superuser = models.BooleanField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

class Location(models.Model):
    county = models.CharField(max_length=50, blank=True, null=True)
    sub_county = models.CharField(max_length=50, blank=True, null=True)
    village_or_estate = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return "%s, %s" %(self.village_or_estate,self.county)

class ApplicationClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    main_phone_number = models.IntegerField(blank=True, null = True)
    alt_phone_number = models.IntegerField(blank=True, null = True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    location = models.ForeignKey(Location, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s %s" %(self.user.first_name,self.user.last_name)

class ClientEmergencyContact(models.Model):
    client = models.OneToOneField(ApplicationClient, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    relation = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    main_phone_number = models.IntegerField(blank=True, null = True)
    alt_phone_number = models.IntegerField(blank=True, null = True)

    def __str__(self):
        return "%s %s" %(self.first_name,self.last_name)

locations = Location
clients = ApplicationClient
emergy_contacts = ClientEmergencyContact
