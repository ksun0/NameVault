import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from tracker.models import Name

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):

    email       = models.EmailField(blank=True, unique=True)
    is_active    = models.BooleanField(default=True)
    is_admin     = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    date_joined  = models.DateTimeField(_('date joined'), default=timezone.now)
    names = models.ManyToManyField(Name)
    # is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.email

    def get_short_name(self):
        "Returns the short name for the user."
        return self.email

    def email_user(self, subject, message, from_email=None, html_message=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], html_message=html_message)
