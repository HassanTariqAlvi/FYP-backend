from app.models import SalarySlip


class SalarySlipService:
    def save_salary_slip(self, **kwargs):
        SalarySlip.objects.create(**kwargs)
