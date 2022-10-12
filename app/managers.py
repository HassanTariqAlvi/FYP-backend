import datetime

from django.contrib.auth.models import BaseUserManager, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction

from app import models as app_models
from django.contrib.auth.models import GroupManager


class CustomerManager(models.Manager):

    def __get_model_fields(self):
        model_fields = []
        for field in self.model._meta.concrete_fields:
            if field is not 'created_at':
                model_fields.append(field.name)
        return model_fields

    def __instance_to_dict(self, instance):
        data = {}
        for field in instance._meta.concrete_fields:
            if isinstance(field.value_from_object(instance), datetime.date):
                data[field.name] = field.value_from_object(
                    instance).strftime("%m/%d/%Y")
            elif field.name == 'image':
                pass
            else:
                data[field.name] = field.value_from_object(instance)
        return data

    def __get_updated_fields(self, instance_dict, old_instance):
        updated_fields = []
        fields = self.__get_model_fields()
        for field in fields:
            if field is not 'created_at' and field is not 'image' and instance_dict[field] != old_instance[field]:
                updated_fields.append(field)
        return updated_fields

    def create(self, user, **kwargs):
        instance = self.model(**kwargs, user=user)
        instance.save()
        return instance

    def update(self, user, id, **kwargs):
        instance = self.model.objects.get(pk=id)
        content_type = ContentType.objects.get(
            model=self.model._meta.model_name)

        old_instance_dict = self.__instance_to_dict(instance)
        with transaction.atomic():
            instance = self.perform_update(instance, **kwargs)
            instance_dict = self.__instance_to_dict(instance)
            updated_fields = self.__get_updated_fields(
                instance_dict,
                old_instance_dict
            )
            if len(updated_fields) != 0:
                comment = self.__get_comment(updated_fields)

                reversion_revision = app_models.ReversionRevision.objects.create(
                    comment=comment,
                    user=user
                )
                app_models.ReversionVersion.objects.create(
                    object_id=instance.id,
                    format='json',
                    serialized_data={
                        'previous_data': old_instance_dict,
                        'new_data': instance_dict
                    },
                    content_type=content_type,
                    revision=reversion_revision
                )
            return instance

    def perform_update(self, instance, **kwargs):
        pass

    def __get_comment(self, updated_fields):
        model_name = self.model._meta.model_name.capitalize()
        comment = f'{model_name} data updated in '
        for f in updated_fields:
            comment += f'{f}, '
        comment = comment[:-2] + \
            (" field" if len(updated_fields) == 1 else " fields")
        return comment


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, employee=None, **extra_fields):
        if not username:
            raise ValueError('User must have the username')

        with transaction.atomic():
            user = self.model(
                username=username,
                employee=employee,
            )

            if 'is_active' in extra_fields:
                user.is_active = extra_fields['is_active']
            if 'is_staff' in extra_fields:
                user.is_staff = extra_fields['is_staff']

            user.set_password(password)
            user.save(using=self._db)

            user_group = app_models.UserGroup.objects.get(
                name=extra_fields['user_group'])
            user.groups.add(user_group)

            user.user_permissions.clear()
            for permission in user_group.permissions.all():
                user.user_permissions.add(permission)

            return user

    def create_superuser(self, username, password=None, employee=None, **extra_fields):
        if not username:
            raise ValueError('User must have the username')

        with transaction.atomic():
            user = self.model(
                username=username,
                employee=employee,
                is_staff=True,
                is_active=True,
                is_superuser=True
            )
            user.set_password(password)
            user.save(using=self._db)

            for permission in Permission.objects.all():
                user.user_permissions.add(permission)
            return user

    def update_user(self, **kwargs):
        instance = self.model.objects.get(username=kwargs['username'])

        with transaction.atomic():
            user_group = app_models.UserGroup.objects.get(
                name=kwargs['user_group'])

            instance.is_staff = kwargs['is_staff']
            instance.is_active = kwargs['is_active']
            instance.is_superuser = kwargs['is_superuser']

            if instance.password != kwargs['password']:
                instance.set_password(kwargs['password'])

            instance.groups.clear()
            instance.groups.add(user_group)

            instance.user_permissions.clear()
            for permission in user_group.permissions.all():
                instance.user_permissions.add(permission)

            instance.save(using=self._db)

    def update_superuser(self, **kwargs):
        instance = self.model.objects.get(username=kwargs['username'])

        with transaction.atomic():
            instance.is_staff = True
            instance.is_active = True
            instance.is_superuser = True

            if instance.password != kwargs['password']:
                instance.set_password(kwargs['password'])

            instance.user_permissions.clear()
            for permission in Permission.objects.all():
                instance.user_permissions.add(permission)

            instance.save(using=self._db)


class DepartmentManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.name = kwargs['name']
        instance.save()
        return instance


class EmployeeTypeManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.name = kwargs['name']
        instance.save()
        return instance


class EmployeeManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.name = kwargs['name']
        instance.city = kwargs['city']
        instance.cnic = kwargs['cnic']
        if 'image' in kwargs.keys():
            instance.image = kwargs['image']
        if kwargs['employee_type'].name != 'Contract':
            instance.role = kwargs['role']
        elif kwargs['employee_type'].name == 'Contract':
            instance.role = None
        instance.gender = kwargs['gender']
        instance.address = kwargs['address']
        instance.phone_no = kwargs['phone_no']
        instance.department = kwargs['department']
        instance.joining_date = kwargs['joining_date']
        instance.employee_type = kwargs['employee_type']
        instance.save()
        return instance


class MeasureCriteriaManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.name = kwargs['name']
        instance.quantity = kwargs['quantity']
        instance.save()
        return instance


class UnitManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.name = kwargs['name']
        instance.save()
        return instance


class UnitPriceManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.unit = kwargs['unit']
        instance.criteria = kwargs['criteria']
        instance.department = kwargs['department']
        instance.price = kwargs['price']
        instance.save()
        return instance

    def get_unit_price(self, kwargs):
        return self.model.objects.filter(**kwargs).first()


class DailyWorkManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.employee = kwargs['employee']
        instance.unit_price = kwargs['unit_price']
        instance.total_pieces = kwargs['total_pieces']
        instance.price_per_unit = kwargs['price_per_unit']
        instance.total_amount = kwargs['total_amount']
        instance.save()
        return instance


class LoanManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.employee = kwargs['employee']
        instance.description = kwargs['description']
        instance.loan_amount = kwargs['loan_amount']
        instance.save()
        return instance


class LoanDetailManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        instance.employee = kwargs['employee']
        instance.total_loan_left = kwargs['total_loan_left']
        instance.loan_pending = kwargs['loan_pending']
        instance.save()
        return instance


class LoanRecoveryManager(CustomerManager):
    def create(self, user, **kwargs):
        with transaction.atomic():
            loanDetail = kwargs['loanDetail']
            # self.model.objects.create(
            #     loanDetail=loanDetail,
            #     deducted_amount=kwargs['deducted_amount'],
            #     user=user
            # )
            loanDetail.total_loan_left -= kwargs['deducted_amount']
            loanDetail.loan_pending = True if loanDetail.total_loan_left > 0 else False
            loanDetail.save()
            return super().create(user, **kwargs)


class RoleManager(CustomerManager):
    def perform_update(self, instance, **kwargs):
        # instance.name = kwargs['name']
        # instance.save()
        return instance


class UserGroupManager(GroupManager):
    def create(self, **kwargs):
        with transaction.atomic():
            user_group = self.model(name=kwargs['name'])
            user_group.save()

            for permission in kwargs['permissions']:
                user_group.permissions.add(permission)
        return user_group

    def update(self, **kwargs):
        with transaction.atomic():
            user_group = self.model.objects.get(pk=kwargs['id'])
            user_group.name = kwargs['name']
            user_group.save()

            user_group.permissions.clear()
            for permission in kwargs['permissions']:
                user_group.permissions.add(permission)
        return user_group


class OverTimeManager(CustomerManager):
    def update(self, id, user, **kwargs):
        overtime = self.model.objects.get(pk=id)
        overtime.date = kwargs['date']
        overtime.start = kwargs['start']
        overtime.end = kwargs['end']
        overtime.worked_hours = kwargs['worked_hours']
        overtime.save()
        return overtime


class SalaryGenerationManager(CustomerManager):
    def create(self, user, **kwargs):
        instance = self.model(
            user=user,
            generate_date=kwargs['generate_date'],
            generate_time=kwargs['generate_time'],
        )
        instance.save()
