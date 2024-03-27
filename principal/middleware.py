from django.shortcuts import render

# meuapp/middleware/theme_middleware.py

class ThemeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'theme' in request.COOKIES:
            theme = request.COOKIES['theme']
            if theme == 'dark':
                request.theme = 'dark'
                request.font = 'light'
            else:
                request.theme = 'light'
                request.font = 'dark'
        else:
            request.theme = 'dark'
            request.font = 'light'
        
        response = self.get_response(request)
        return response
