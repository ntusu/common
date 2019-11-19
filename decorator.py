from functools import wraps

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from rest_framework.response import Response
from rest_framework.decorators import api_view as drf_api_view


def api_view(http_method_schemas, form=None, serializer=None):
    def decorator(func):
        @wraps(func)
        @drf_api_view(http_method_schemas)
        def _func(request, *args, **kwargs):
            if form is not None:
                if request.method == 'GET':
                    data_form = form(request.query_params)
                else:
                    data_form = form(request.data)
                if not data_form.is_valid():
                    return Response({'success': False, 'errors': 'Invalid arguments'}, status=400)
                data = data_form.cleaned_data
                return func(request, data=data, *args, **kwargs)
            elif serializer is not None:
                if request.method == 'GET':
                    data_serializer = serializer(data=request.query_params)
                else:
                    data_serializer = serializer(data=request.data)
                if not data_serializer.is_valid():
                    return Response({'success': False, 'errors': 'Invalid arguments'}, status=400)
                data = data_serializer.data
                return func(request, data=data, *args, **kwargs)
            return func(request, *args, **kwargs)
        return _func
    return decorator


def paginator_helper(qs, page_size=10, page=1):
    paginator = Paginator(qs, page_size)
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)
    return result
