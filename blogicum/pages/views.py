from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def not_found_page(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_forbidden_page(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def internal_error_page(request):
    return render(request, 'pages/500.html', status=500)
