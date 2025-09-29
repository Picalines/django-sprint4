from django.shortcuts import render
from django.views.generic import TemplateView


class AboutPage(TemplateView):
    template_name = 'pages/about.html'


class RulesPage(TemplateView):
    template_name = 'pages/rules.html'


class LogoutPage(TemplateView):
    """
    Временный view до https://github.com/yandex-praktikum/django-sprint4/pull/1

    Вкратце: тесты ищут *первую* форму во всей разметке. Из-за этого нельзя
    добавить форму logout в header.html - нужно чтобы она жила на отдельной
    странице. Это и делает этот view
    """

    template_name = 'pages/logout.html'


def not_found_page(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_forbidden_page(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def internal_error_page(request):
    return render(request, 'pages/500.html', status=500)
