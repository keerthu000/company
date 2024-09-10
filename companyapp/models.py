from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomerUser(AbstractUser):
    # Role-specific Boolean fields
    is_admin = models.BooleanField(default=False)
    is_hr_manager = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    # Optional: Use email as the username for authentication
    email = models.EmailField(unique=True)
    
    # Define which field will be used as the username for authentication
    USERNAME_FIELD = 'email'
    # 'username' and 'password' are required by default, you can add others here
    REQUIRED_FIELDS = []  # No additional required fields, just email and password

    # Overriding groups field to customize it
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_groups'  # Custom related name for groups
    )

    # Overriding user_permissions field to customize it
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions'  # Custom related name for permissions
    )

class Company(models.Model):
    is_admin = models.BooleanField(default=False)
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE,null=True, blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True,default=None)
    address = models.CharField(max_length=200,null=True,blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True,default=None)
    password = models.CharField(max_length=100, null=True, blank=True)  # For demo purposes; use hashing for passwords
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)



    

    

class Hr_manger(models.Model):
    is_hr_manager = models.BooleanField(default=False)
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE,null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    hr_name=models.CharField(max_length=100, null=True, blank=True,default=None)
    address = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True,default=None)
    password = models.CharField(max_length=100, null=True, blank=True)




class Manger(models.Model):
    is_manager = models.BooleanField(default=False)
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE,null=True, blank=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    mngr_name=models.CharField(max_length=100, null=True, blank=True,default=None)
    address = models.CharField(max_length=200, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True,default=None)
    password = models.CharField(max_length=100, null=True, blank=True)


class Departments(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, null=True, blank=True)

class Role(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, null=True, blank=True)



class Employee(models.Model):
    is_employee = models.BooleanField(default=False)
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE,null=True, blank=True)
    company=models.ForeignKey(Company,on_delete=models.CASCADE, null=True, blank=True)
    
    emp_name=models.CharField(max_length=100, null=True, blank=True,default=None)
    emp_id= models.CharField(max_length=10,  blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True,default=None)
    password = models.CharField(max_length=100, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    joining_date=models.DateField(max_length=20, null=True, blank=True)
    salary=models.CharField(max_length=20, null=True, blank=True)


class Attendance(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE, null=True, blank=True)
    manager=models.ForeignKey(Manger,on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    clock_in = models.DateTimeField()
    clock_out = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)

class LeaveRequest(models.Model):
    company=models.ForeignKey(Company,on_delete=models.CASCADE, null=True, blank=True)
    manager=models.ForeignKey(Manger,on_delete=models.CASCADE, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    


