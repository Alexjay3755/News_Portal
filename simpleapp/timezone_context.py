import pytz
from django.utils import timezone


def get_timezone(request):
    return {
        'current_time': timezone.now(),
        'timezones': pytz.common_timezones
    }