from django.shortcuts import redirect
from django.urls import reverse


class NoPermissionRedirectMixin:
    no_permission_url = None
    no_permission_kwargs = None

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        kwargs_to_pass = self.no_permission_kwargs or [self.pk_url_kwarg]
        passed_kwargs = {kwarg: self.kwargs[kwarg] for kwarg in kwargs_to_pass}

        return redirect(reverse(self.no_permission_url, kwargs=passed_kwargs))
