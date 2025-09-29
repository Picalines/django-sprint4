from django.urls import path

from .views import AboutPage, LogoutPage, RulesPage

app_name = "pages"

urlpatterns = [
    path("about/", AboutPage.as_view(), name="about"),
    path("rules/", RulesPage.as_view(), name="rules"),
    path('auth/logout/', LogoutPage.as_view(), name='logout'),
]
