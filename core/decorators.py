from functools import wraps

from django.http import HttpResponseForbidden


def require_htmx(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        """Validates that a view is being called from a HTMX request."""
        if request.headers.get('HX-Request', '') == 'true':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Access Denied")
    return _wrapped_view