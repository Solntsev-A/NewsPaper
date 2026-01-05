import pytz
from django.utils import timezone

def timezone_context(request):
    return {
        'timezones': pytz.common_timezones,
        'TIME_ZONE': timezone.get_current_timezone_name(),
    }