import os
import random

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 2541781232)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "accounts/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)
#Create a UserManager for class User
class UserManager(models.Manager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    # q
    def create_staffuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



    # password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True
    # q: are you there?
    # a: yes
    # q: what is the function of line 74-75?
    # a: it is used to check if the user has permission to view the page

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.is_active

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'username']

    objects = UserManager()

class Service(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Region(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile (models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE , blank=False, null=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE , blank=False, null=False)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    contact = models.CharField(max_length=20, blank=False, null=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_object(self):
        return get_object_or_404(UserProfile, user__username=self.kwargs['username'])

    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True

