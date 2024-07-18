from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import reverse


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

    def get_login_redirect_url(self, user):
        if user.user_type in ['owner', 'admin']:
            return reverse('admin_dashboard')
        elif user.user_type == 'seller':
            return reverse('seller_dashboard')
        else:
            return reverse('customer_dashboard')
