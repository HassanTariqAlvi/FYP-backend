from django.contrib import admin
from app.models import *
from django.contrib.auth.models import Permission


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    list_display = ['id', 'content_type_id', 'codename',
                    'name']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'username', 'employee',
                    'is_active', 'is_staff', 'is_superuser']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = ['id', 'name', 'user',  'created_at']


@admin.register(EmployeeType)
class EmployeeTypeAdmin(admin.ModelAdmin):
    model = EmployeeType
    list_display = ['id', 'name', 'user', 'created_at']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    model = Role
    list_display = ['id',
                    'name', 'salary', 'user', 'created_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    list_display = ['id', 'name', 'cnic', 'phone_no', 'gender', 'city', 'address', 'department', 'employee_type', 'role',
                    'joining_date', 'image', 'user',  'created_at']


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    model = Salary
    list_display = ['id', 'employee', 'from_date', 'to_date', 'total_salary', 'net_salary', 'issue_date', 'user',
                    'created_at', 'paid_by', 'paid']


@admin.register(SalarySlip)
class SalarySlipAdmin(admin.ModelAdmin):
    model = SalarySlip
    list_display = ['id', 'salary', 'is_loan_deducted',
                    'loanRecovery', 'created_at', 'user']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    model = Attendance
    list_display = ['id', 'employee', 'emp_in',
                    'emp_out', 'worked_hours', 'date', 'user',  'created_at']


@admin.register(OverTime)
class OverTimeAdmin(admin.ModelAdmin):
    model = OverTime
    list_display = ['id', 'employee', 'start',
                    'end', 'worked_hours', 'date', 'user',  'created_at']


@admin.register(SalaryGeneration)
class SalaryGenerationAdmin(admin.ModelAdmin):
    model = SalaryGeneration
    list_display = ['id', 'generate_date',
                    'generate_time', 'user',  'created_at']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    model = Unit
    list_display = ['id', 'name', 'user', 'created_at']


@admin.register(MeasureCriteria)
class MeasureCriteriaAdmin(admin.ModelAdmin):
    model = MeasureCriteria
    list_display = ['id', 'name', 'quantity', 'user', 'created_at']


@admin.register(UnitPrice)
class UnitPriceAdmin(admin.ModelAdmin):
    model = UnitPrice
    list_display = ['id', 'unit', 'department', 'criteria', 'price',  'user',
                    'created_at']


@admin.register(DailyWork)
class DailyWorkAdmin(admin.ModelAdmin):
    model = DailyWork
    list_display = ['id', 'employee_id', 'unit_price_id', 'total_pieces', 'price_per_unit', 'total_amount', 'date',
                    'user', 'created_at']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    model = Loan
    list_display = ['id', 'employee', 'loan_amount', 'description', 'apply_date', 'status',
                    'user', 'created_at']


@admin.register(LoanDetail)
class LoanDetailAdmin(admin.ModelAdmin):
    model = LoanDetail
    list_display = ['employee', 'total_loan_left',
                    'loan_pending',  'user', 'created_at']


@admin.register(LoanRecovery)
class LoanRecoveryAdmin(admin.ModelAdmin):
    model = LoanRecovery
    list_display = ['id', 'loanDetail', 'deducted_amount',
                    'recovery_date',  'user', 'created_at']


# @admin.register(UserGroup)
# class UserGroupAdmin(admin.ModelAdmin):
#     model = UserGroup
#     list_display = ['id', 'name']
