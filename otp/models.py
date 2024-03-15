from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password, is_staff=False, is_active=False, is_admin=False, ):
        if not phone:
            raise ValueError('telefon raqam kiritishingiz shart!')
        if not password:
            raise ValueError('maxfiy kod kiriting:')
        user = self.model(
            phone=phone,
            password = password
        )
        user.save(using=self._db)
        return user
    
    

    def create_staffuser(self, phone, password,):
        user = self.create_user(
            phone = phone,
            password=password,
        )
        return user

    def create_superuser(self, phone, password, is_staff=True, is_active=True, is_admin=True,):
        user = self.create_user(
            phone = phone,
            password=password,
            is_staff=True,
            is_active=True,
            is_admin=True,
        )
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

def upload_location(instace, filename, **kwargs):
    file_path='blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instace.id), title=str(instace.name), filename=filename
    )
    return file_path

class User(AbstractBaseUser):
        phone_regex=RegexValidator(regex='d{0,9}', message="Telefon raqamini +9989XXXXXXXX kabi kiriting!")
        phone=models.CharField(validators=[phone_regex],max_length=9,unique=True) 
        otp = models.CharField(max_length=9, blank=True, null=True)
        name = models.CharField(max_length=100)
        image = models.ImageField(upload_to=upload_location, null=True, blank=True)
        date_uploadated = models.DateTimeField(auto_now=True, verbose_name='yangilash vaqti')
        date_published = models.DateTimeField(auto_now_add=True, verbose_name='nashr vaqti')
        staff = models.BooleanField(default=True)
        active = models.BooleanField(default=True)
        admin = models.BooleanField(default=False)
        objects = UserManager()

        username = None
        email=None

        USERNAME_FIELD = 'phone'
        REQUIRED_FIELD = ['name']

        def __str__(self):
            return self.phone

        @property
        def is_active(self):
            return self.active

        @property
        def is_admin(self):
            return self.admin

        @property
        def is_staff(self):
            return self.staff

        @property
        def is_superuser(self):
            return self.is_admin

        def has_perm(self, perm, obj=None):
            return True

        def has_module_perms(self, app_label):
            return True

        @property
        def is_staff(self):
            return self.is_admin

# Create your models here.zzz
class PhoneOtp(models.Model):
    phone_regex=RegexValidator(regex='d{0,9}', message="Telefon raqamini +9989XXXXXXXX kabi kiriting!")
    phone=models.CharField(validators=[phone_regex],max_length=9,unique=True) 
    def __str__(self):
        massage=str(self.phone)+"ga jo'natildi"+str(self.otp)
        return massage

    

class ValidatedOtp(models.Model):
    phone_regex = RegexValidator(regex='d{0,9}', message="Telefon raqamini +9989XXXXXXXX kabi kiriting!")
    phone = models.CharField(validators=[phone_regex],max_length=9,unique=True) 
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Kodni kiritishlar soni:')
    validated = models.BooleanField(default=False, help_text="Shaxsiy kabinetingizni yaratishingiz mumkin!")

    def __str__(self):
        return str(self.phone)


class Verification(models.Model):
    STATUS = (
        ('send', 'send'),
        ('confirmed', 'confirmed'),
    )
    phone = models.CharField(max_length=9, unique=True)
    verify_code = models.SmallIntegerField()
    is_verified = models.BooleanField(default=False)
    step_reset = models.CharField(max_length=10, null=True, blank=True, choices=STATUS)
    step_change_phone = models.CharField(max_length=30, null=True, blank=True, choices=STATUS)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} --- {self.verify_code}"