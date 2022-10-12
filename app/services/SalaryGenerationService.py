from app.models import SalaryGeneration
from app.exceptions import AlreadyExists


class SalaryGenerationService:
    def get_all_salary_generations(self):
        return SalaryGeneration.objects.all()

    def check_salary_generated_or_not(self, date):
        all_generations = self.get_all_salary_generations()
        for record in all_generations:
            if record.generate_date.month == date.month and record.generate_date.year == date.year:
                raise AlreadyExists(
                    detail="Salaries are already generated")
