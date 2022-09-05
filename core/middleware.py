from django.utils.timezone import now
from api.models import User

class SetLastRequestMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
      
        response = self.get_response(request)
        if request.user.is_authenticated:  
            # Update last visit time after request finished processing.
            current_user = User.objects.filter(pk=request.user.pk)
            current_user.update(last_request=now())
        
        return response
