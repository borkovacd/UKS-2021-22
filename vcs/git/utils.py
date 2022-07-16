from functools import wraps
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def request_passes_test(test_func, login_url=None):
    """
    Decorator for views that checks that the session passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the request object and returns True if the test passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request, **kwargs):
                return view_func(request, *args, **kwargs)
            else:
                if login_url:
                    return redirect(login_url)
                else:
                    raise PermissionDenied()
        return _wrapped_view
    return decorator
