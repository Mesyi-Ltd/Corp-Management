from main.models import Staff, MonthlyPerformance, AnnualPerformance
from datetime import datetime


def reset_monthly_performance():
    staffs = Staff.objects.all()
    month, year = datetime.now().month, datetime.now().year
    for staff in staffs:
        perf = MonthlyPerformance.objects.create(owner=staff, year=year, month=month)
        perf.save()


def reset_annual_performance():
    staffs = Staff.objects.all()
    year = datetime.now().year
    for staff in staffs:
        perf = AnnualPerformance.objects.create(owner=staff, year=year)
        perf.save()
