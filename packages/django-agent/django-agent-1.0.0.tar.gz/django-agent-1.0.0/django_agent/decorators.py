from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden


def agent_token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        agent_token = request.META.get('HTTP_AGENT_TOKEN')

        if agent_token != settings.AGENT_TOKEN:
            return HttpResponseForbidden("Invalid Agent Token")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
