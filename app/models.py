from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.managers import *


class AbstractBaseModel(models.Model):
    """
    Abstract Base Model
    """
    user = models.ForeignKey('User', on_delete=models.RESTRICT)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

# ---------------------------------------------------------------------


class Department(models.Model):
    """
    Department model
    """
    name = models.CharField(max_length=50)
    user = models.ForeignKey('User', on_delete=models.RESTRICT)
    created_at = models.DateField(auto_now_add=True)

    objects = DepartmentManager()

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------


class DailyWork(AbstractBaseModel):
    """
    Daily work model
    """
    employee = models.ForeignKey('Employee', on_delete=models.RESTRICT)
    unit_price = models.ForeignKey(
        'UnitPrice', on_delete=models.RESTRICT)
    total_pieces = models.CharField(max_length=3)
    price_per_unit = models.FloatField()
    total_amount = models.FloatField()
    # date = models.DateField(auto_now_add=True)
    date = models.DateField()

    objects = DailyWorkManager()

    class Meta:
        ordering = ['date']
        permissions = [
            ('generateReport_dailywork', 'Can generate daily work report'),
        ]

# ---------------------------------------------------------------------


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Employee(AbstractBaseModel):
    """
    Employee model
    """
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]

    name = models.CharField(max_length=50)
    city = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=12)
    address = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to=upload_to, default="")
    cnic = models.CharField(max_length=15, unique=True)
    department = models.ForeignKey('Department', on_delete=models.RESTRICT)
    employee_type = models.ForeignKey(
        'EmployeeType', on_delete=models.RESTRICT)
    role = models.ForeignKey(
        'Role', on_delete=models.RESTRICT, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER)
    joining_date = models.DateField()
    user = models.ForeignKey(
        'User', on_delete=models.RESTRICT, related_name="user")

    objects = EmployeeManager()

    def __str__(self):
        return str(self.id)


# ---------------------------------------------------------------------


class EmployeeType(AbstractBaseModel):
    """
    Employee type model
    """
    name = models.CharField(max_length=50, unique=True)

    objects = EmployeeTypeManager()

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------


class Role(AbstractBaseModel):
    name = models.CharField(max_length=255, unique=True)
    salary = models.IntegerField()

    objects = RoleManager()

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------


class LoanDetail(AbstractBaseModel):
    """
    Loan detail model
    """
    employee = models.OneToOneField(
        'Employee', on_delete=models.RESTRICT, primary_key=True)
    total_loan_left = models.IntegerField()
    loan_pending = models.BooleanField()

    objects = LoanDetailManager()

    class Meta:
        permissions = [
            ('generateReport_loandetail', 'Can generate loan detail report'),
        ]

    def __str__(self):
        return str(self.employee)

# ---------------------------------------------------------------------


class Loan(AbstractBaseModel):
    """
    Loan model
    """
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    STATUS = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    employee = models.ForeignKey('Employee', on_delete=models.RESTRICT)
    loan_amount = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length=8, choices=STATUS, default='Pending')
    # apply_date = models.DateField(auto_now=True)
    apply_date = models.DateField()

    objects = LoanManager()

    class Meta:
        permissions = [
            ('approveLoan_loan', 'Can approve or reject loan application'),
            ('viewLoanApplicationStatus_loan', 'Can view loan application status'),
        ]

    def __str__(self):
        return str(self.id)

# ---------------------------------------------------------------------


class LoanRecovery(AbstractBaseModel):
    """
    Loan recovery model
    """
    loanDetail = models.ForeignKey('LoanDetail', on_delete=models.RESTRICT)
    deducted_amount = models.IntegerField()
    recovery_date = models.DateField()
    # recovery_date = models.DateField(auto_now=True)

    objects = LoanRecoveryManager()

    class Meta:
        permissions = [
            ('generateReport_loanrecovery', 'Can generate loan recovery report'),
        ]

    def __str__(self):
        return str(self.id)

# ---------------------------------------------------------------------


class MeasureCriteria(AbstractBaseModel):
    """
    Measure criteria model
    """
    name = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField()

    objects = MeasureCriteriaManager()

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------


class Unit(AbstractBaseModel):
    """
    Units model
    """
    name = models.CharField(max_length=50, unique=True)

    objects = UnitManager()

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------


class UnitPrice(AbstractBaseModel):
    """
    Units price model
    """
    unit = models.ForeignKey('Unit', on_delete=models.RESTRICT)
    department = models.ForeignKey('Department', on_delete=models.RESTRICT)
    criteria = models.ForeignKey('MeasureCriteria', on_delete=models.RESTRICT)
    price = models.FloatField()

    objects = UnitPriceManager()

    class Meta:
        unique_together = ('unit', 'department', 'criteria')

    def __str__(self):
        return str(self.id)

# ---------------------------------------------------------------------


class Salary(AbstractBaseModel):
    """
    Salary model
    """
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    total_salary = models.IntegerField()
    net_salary = models.IntegerField()
    issue_date = models.DateField(null=True)
    paid_by = models.ForeignKey(
        'User', on_delete=models.RESTRICT, related_name="paid_by_user", null=True)
    paid = models.BooleanField()

    class Meta:
        permissions = [
            ('generate_salary', 'Can generate salary'),
            ('pay_salary', 'Can pay salary'),
            ('generateReport_salary', 'Can generate salary report'),
        ]

    def __str__(self):
        return str(self.id)


# ---------------------------------------------------------------------


class SalarySlip(AbstractBaseModel):
    """
    Salary slip model
    """
    salary = models.OneToOneField('Salary', on_delete=models.RESTRICT)
    is_loan_deducted = models.BooleanField(default=False)
    loanRecovery = models.OneToOneField(
        'LoanRecovery', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return str(self.id)

# ---------------------------------------------------------------------


class Attendance(AbstractBaseModel):
    """
    Attendance model
    """
    employee = models.ForeignKey('Employee', on_delete=models.RESTRICT)
    emp_in = models.TimeField()
    emp_out = models.TimeField(null=True)
    worked_hours = models.FloatField(default=0)
    date = models.DateField()

    class Meta:
        permissions = [
            ('generateReport_attendance', 'Can generate attendance report'),
        ]

# ---------------------------------------------------------------------


class OverTime(AbstractBaseModel):
    """
    Over time model
    """
    employee = models.ForeignKey('Employee', on_delete=models.RESTRICT)
    start = models.TimeField()
    end = models.TimeField()
    worked_hours = models.FloatField(default=0)
    date = models.DateField()

    objects = OverTimeManager()

# ---------------------------------------------------------------------


class UserGroup(models.Model):
    name = models.CharField(_("name"), max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    objects = UserGroupManager()

    class Meta:
        verbose_name = _("usergroup")
        verbose_name_plural = _("usergroups")

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

# ---------------------------------------------------------------------


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
    )
    employee = models.OneToOneField(
        'Employee', on_delete=models.CASCADE, null=True, related_name='employee')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        UserGroup,
        verbose_name=_("groups"),
        blank=True,
        related_name="user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'username'

    objects = UserManager()

# ---------------------------------------------------------------------


class ReversionRevision(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# ---------------------------------------------------------------------


class ReversionVersion(models.Model):
    object_id = models.IntegerField()
    format = models.CharField(max_length=10)
    serialized_data = models.JSONField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    revision = models.ForeignKey('ReversionRevision', on_delete=models.CASCADE)

# ---------------------------------------------------------------------


class SalaryGeneration(AbstractBaseModel):
    generate_date = models.DateField()
    generate_time = models.TimeField()

    objects = SalaryGenerationManager()
