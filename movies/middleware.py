from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin

class RequestCounterMiddleware(MiddlewareMixin):
    def __call__(self, request):
        # Increment the count in the cache
        count = cache.get('request_count', 0)
        cache.set('request_count', count + 1)
        response = self.get_response(request)
        return response
