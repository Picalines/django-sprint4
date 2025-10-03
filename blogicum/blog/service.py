from django.core.paginator import Paginator


def get_page_obj(request, objects, objects_per_page):
    return Paginator(objects, objects_per_page).get_page(
        request.GET.get('page')
    )
