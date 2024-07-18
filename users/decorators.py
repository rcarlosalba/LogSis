from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def user_type_required(*allowed_types):
    def check_user_type(user):
        if user.user_type in allowed_types:
            return True
        raise PermissionDenied
    return user_passes_test(check_user_type)
