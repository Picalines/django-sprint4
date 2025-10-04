from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse


class UserIsAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user == self.get_object().author


class SuccessUrlArgsMixin:
    success_url = None

    def get_success_url_args(self):
        return []

    def get_success_url(self):
        return reverse(self.success_url, args=self.get_success_url_args())


class NoPermissionRedirectMixin:
    no_permission_url = None
    no_permission_kwargs = None

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()

        kwargs_to_pass = self.no_permission_kwargs or [self.pk_url_kwarg]
        passed_kwargs = {kwarg: self.kwargs[kwarg] for kwarg in kwargs_to_pass}

        return redirect(reverse(self.no_permission_url, kwargs=passed_kwargs))


class SubListMixin:
    paginate_sublist_by = None

    def get_sublist_queryset(self):
        raise NotImplementedError(
            'SubListMixin.get_sublist_queryset is not implemented'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Paginator(
            self.get_sublist_queryset(),
            self.paginate_sublist_by,
        ).get_page(self.request.GET.get('page'))
        return context
