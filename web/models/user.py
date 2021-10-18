from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from .achievement import Achievement


class UserManager(BaseUserManager):

    def create_user(self, email, password, birthday, name=None):
        if not email:
            raise ValueError('Users must have an email address')

        if name is None:
            name = email[:email.find('@')]

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            birthday=birthday
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Moderator')
    is_superuser = models.BooleanField(default=False, verbose_name='Admin')

    name = models.CharField(max_length=50, blank=True)
    premium = models.BooleanField(default=False)
    birthday = models.DateField(blank=True, null=True)
    achievement = models.ManyToManyField(Achievement, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "auth_user"
