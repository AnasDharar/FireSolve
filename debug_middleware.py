from django.http import HttpResponse

class DebugHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"[DEBUG] Host header received: {request.get_host()}")
        return self.get_response(request)
