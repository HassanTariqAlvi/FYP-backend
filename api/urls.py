from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from api.views import *
from .views.GroupView import GroupView

router = routers.DefaultRouter()

router.register(r'hrm/loan', LoanView, basename="loan")
router.register(r'hrm/departments', DepartmentView, basename="departments")
router.register(r'hrm/employee/details', EmployeeView,
                basename="employee_details")
router.register(r'hrm/loan_detail',
                LoanDetailView, basename="loan_detail")
router.register(r'hrm/employee/attendance', AttendanceView,
                basename="employee_details")
router.register(r'hrm/loan_recovery',
                LoanRecoveryView, basename="loan_recovery")
router.register(r'hrm/employee/employee_type',
                EmployeeTypeView, basename="employee_types")

router.register(r'hrm/employee/overtime',
                OverTimeView, basename="overtime")


router.register(r'units/unit_details',
                UnitView, basename="units")
router.register(
    r'units/unit_prices', UnitPriceView, basename="units_price")
router.register(r'units/measure_criteria',
                MeasureCriteriaView, basename="measure_criteria")

router.register(r'hrm/salary', SalaryView, basename="salary")

router.register(r'daily_work', DailyWorkView, basename="daily_work")

router.register(r'users', UserView, basename="users")
router.register(r'permissions', PermissionView,
                basename="permissions")
router.register(r'hrm/employee/roles', RoleView, basename="roles")
router.register(r'system_users/groups', GroupView, basename="groups")


urlpatterns = [
    path('', include(router.urls)),
    path('user/login/', UserLoginView.as_view(), name="user_login"),
    path('user/logout/', UserLogoutView.as_view(), name="user_logout"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('reports/',
         ReportsView.as_view(), name='reports'),
    path('stats',
         StatsView.as_view(), name='stats'),
    path('log_files',
         LogFileView.as_view(), name='log_files'),

]
