from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver


class UserManager(BaseUserManager):
  
    use_in_migrations = True
  
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
  
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password=password, **extra_fields)
  
  
class User(AbstractBaseUser, PermissionsMixin):
  
    email = models.EmailField(
        verbose_name = _('email address'),
        unique=True
    )
    first_name = models.CharField(
        verbose_name = _('first name'),
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        verbose_name = _('last name'),
        max_length=150,
        blank=True
    )
    is_staff = models.BooleanField(
        verbose_name = _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        verbose_name = _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_premium = models.BooleanField(
        verbose_name = _('is_premium'),
        default=False,
        help_text=_(
            'プレミアム会員かどうかを示します。'),
    )
    date_joined = models.DateTimeField(
        verbose_name = _('date joined'),
        default=timezone.now
    )
  
    objects = UserManager()
  
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
  
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
  
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in
        between."""
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
  
    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
  
    def send_email(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email