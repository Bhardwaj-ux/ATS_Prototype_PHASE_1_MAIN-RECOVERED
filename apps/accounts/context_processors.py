from django.db.utils import OperationalError, ProgrammingError
from .models import UserPreference


def user_preferences(request):
    if request.user.is_authenticated:
        try:
            prefs, _ = UserPreference.objects.get_or_create(user=request.user)
            display_name = (
                prefs.profile_name
                or request.user.get_full_name()
                or request.user.email
                or request.user.username
            )
            return {
                "user_preferences": prefs,
                "display_name": display_name,
            }
        except (OperationalError, ProgrammingError):
            display_name = (
                request.user.get_full_name()
                or request.user.email
                or request.user.username
            )
            return {
                "user_preferences": None,
                "display_name": display_name,
            }

    return {
        "user_preferences": None,
        "display_name": "",
    }
