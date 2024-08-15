from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from phonenumber_field.modelfields import PhoneNumberField


class MyAccountManager(BaseUserManager):
    def create_user(self, contactNo, password=None):
        if not contactNo:
            raise ValueError('Users must have a contact number')

        user = self.model(
            contactNo=contactNo
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contactNo, password):
        user = self.create_user(
            contactNo = contactNo,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    contactNo = PhoneNumberField(verbose_name="contactNo", unique=True, primary_key=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'contactNo'
    REQUIRED_FIELDS = []

    objects = MyAccountManager()

    # For checking permissions. to keep it simple all admin have ALL permissons

    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return str(self.contactNo)


class Hospital(models.Model):
    hKey = models.IntegerField(primary_key=True)
    hName = models.CharField(max_length=50)
    hAddress = models.CharField(max_length=100)
    hContactNo = PhoneNumberField(null=False, blank=False, unique=True)
    hEmailId = models.EmailField()
    update_ts=models.DateTimeField()

    def __str__(self):
        return self.hName + " Key: " + str(self.hKey)
        #return str(self.update_ts)[:19]


class Operator(models.Model):
    operator = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, primary_key=True)
    oName = models.CharField(max_length=30)
    opStatus = models.CharField(max_length=1)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    opUniqueNotifId = models.CharField(max_length=500)

    def __str__(self):
        return self.oName + "  " + str(self.operator)


class Location(models.Model):
    sensorId = models.CharField(max_length=250,primary_key=True)
    xCor = models.SmallIntegerField()
    yCor = models.SmallIntegerField()
    floorNo = models.SmallIntegerField()
    physicalName = models.CharField(max_length=50,default='Unknown')
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)

    def __str__(self):
        return self.physicalName + " Key: " + self.sensorId


class Client(models.Model):
    client = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, primary_key=True)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    cName = models.CharField(max_length=30)
    gender = models.CharField(max_length=1)
    birthday = models.DateField(default=None)
    occupation = models.CharField(max_length=50)
    workLocation = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    otpField = models.CharField(max_length=6)
    cliUniqueNotifId = models.CharField(max_length=500,blank=True)

    def __str__(self):
        return self.cName + "  " + str(self.client)


class Robot(models.Model):
    macId = models.CharField(max_length=12,primary_key=True)
    rName = models.CharField(max_length=30)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    direction = models.CharField(max_length=1)
    rStatus = models.CharField(max_length=1)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    robUniqueNotifId = models.CharField(max_length=500)

    def __str__(self):
        return self.rName + " Key: " + self.macId


class OrderRequest(models.Model):
    requestId = models.BigAutoField(primary_key=True)
    rGeneratorClient = models.ForeignKey(Client,on_delete=models.CASCADE)
    slocation = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="SenderLocation")
    rlocation = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="ReceiverLocation")
    senMsg = models.CharField(max_length=1000)
    recMsg = models.CharField(max_length=1000)
    reqMsg = models.CharField(max_length=1000)
    ordReqStatus = models.CharField(max_length=1)
    operator = models.ForeignKey(Operator,on_delete=models.CASCADE,blank=True,null=True)
    robot = models.ForeignKey(Robot,on_delete=models.CASCADE,blank=True,null=True)
    created_ts=models.DateTimeField(auto_now_add=True)
    activated_ts=models.DateTimeField(null=True)
    completed_ts=models.DateTimeField(null=True)

    def __str__(self):
        return str(self.requestId)


class Edge(models.Model):
    sensorId1 = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="node1")
    sensorId2 = models.ForeignKey(Location,on_delete=models.CASCADE,related_name="node2")
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sensorId1) + " " + str(self.sensorId2) + " " + str(self.hospital)


class Patient(models.Model):
    bedNumber = models.CharField(primary_key=True,max_length=10)
    wardNumber = models.CharField(max_length=10)
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    pName = models.CharField(max_length=30)
    age = models.CharField(max_length=30)

    def __str__(self):
        return self.pName + " Key:" + self.bedNumber

class PubsubKey(models.Model):
    pub_key=models.CharField(max_length=100)
    sub_key=models.CharField(max_length=100)

    def __str__(self):
        return 'pubsubkey'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
