from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        user = self.model(
            email = self.normalize_email(email),
            name  = name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email    = email,
			name     = name,
            password = password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
	email      = models.EmailField(max_length=255, unique=True)
	name       = models.CharField(max_length=255)
	is_active  = models.BooleanField(default=True)
	is_staff   = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(null=True)

	class Meta:
		db_table = 'users'

	objects = UserManager()

	USERNAME_FIELD  = 'email'
	REQUIRED_FIELDS = ['name']
	