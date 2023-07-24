from django.db import models
import uuid
from django.utils import timezone
import datetime


# Create your models here.

STATUS_CHOICES = [
    ("0", "ready"),
    ("1", "online"),
    ("2", "offline"),
    ("4", "block"),
]

CUSTOMER = "cu"
STAFF = "st"

ADMIN_ = "07918"
MANAGER_ = "1"
CUSTOMER_ = "2"
EMPLOYEE_ = "3"
USER_ = "4"

ACTIVE = "user_active"
INACTIVE = "user_inactive"
BLOCK = "block"

USER_LOGIN_TYPE_CHOICES = [
    (ADMIN_, "Admin"),
    (MANAGER_, "Manager"),
    (CUSTOMER_, "Customer"),
    (EMPLOYEE_, "Employee"),
    (USER_, "User"),
]

USER_LOGIN_STATUS_CHOICES = [
    (ACTIVE, "Active"),
    (INACTIVE, "Inactive"),
    (BLOCK, "Block"),
]

USER_TYPE_CHOICES = [
    (ADMIN_, "Admin"),
    (MANAGER_, "Manager"),
    (CUSTOMER_, "Customer"),
    (EMPLOYEE_, "Employee"),
    (USER_, "User"),
]

READY = "re"
UNPAID = "un"
PAID = "pa"
COMPLETE = "co"
PAYS_STATUS_CHOICES = [
    (READY, "Ready"),
    (UNPAID, "Unpaid"),
    (PAID, "Paid"),
    (COMPLETE, "Complete"),
]


class UserManage(models.Manager):
    class Meta:
        proxy = True

    def do_something(self):
        pass


class LoginUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.CharField(null=False, blank=False, max_length=50, unique=True)
    password = models.CharField(null=False, blank=False, max_length=200)
    user_type = models.CharField(null=False, blank=False, choices=USER_LOGIN_TYPE_CHOICES, max_length=50
                                 , default=USER_)
    status = models.CharField(null=False, blank=False, choices=USER_LOGIN_STATUS_CHOICES, max_length=50, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(null=False, blank=False, max_length=50, unique=True)
    name = models.CharField(null=False, blank=False, max_length=50)
    address = models.CharField(null=False, blank=False, max_length=200)
    birthday = models.DateTimeField()
    status = models.CharField(null=False, blank=False, choices=USER_LOGIN_STATUS_CHOICES, default=ACTIVE, max_length=50)
    type_user = models.CharField(null=False, blank=False, choices=USER_TYPE_CHOICES, default=USER_, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=15)
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Commodities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    commodity_name = models.CharField(null=False, blank=False, max_length=200)
    goods_type = models.CharField(null=False, blank=False, max_length=100)
    trademark = models.CharField(null=False, blank=False, max_length=100)
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE)
    count = models.IntegerField(null=False, blank=False)
    remaining_amount = models.IntegerField(null=False, blank=False, default=0)
    price = models.IntegerField(null=False, blank=False)
    image_commodity = models.ImageField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.commodity_name


class ShoppingCart(models.Model):
    ShoppingCart = models.CharField(null=False, blank=True, max_length=100)
    commodity_name = models.ForeignKey(Commodities, on_delete=models.CASCADE)
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE)
    count_cart = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ShoppingCart


class Pays(models.Model):
    pays_name = models.CharField(null=False, blank=True, max_length=100)
    commodity_name = models.ForeignKey(Commodities, on_delete=models.CASCADE)
    count = models.IntegerField(null=False, blank=False)
    user = models.ForeignKey(LoginUser, on_delete=models.CASCADE, null=True)
    user_cache = models.CharField(null=False, blank=True, max_length=200)
    status = models.CharField(null=False, blank=False, choices=PAYS_STATUS_CHOICES, default=READY, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pays_name

