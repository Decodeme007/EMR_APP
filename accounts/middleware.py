# automatically attach the logged-in user's clinic/institution to every request.
'''
Browser Request
      ↓
Middleware
      ↓
Django View
      ↓
Response
      ↓
Middleware
      ↓
Browser
'''

class TenantMiddleware:
    """
    Attaches the current logged-in user's institution (clinic) to request.institution.
    """
    def __init__(self, get_response): #When Django starts, it creates an instance of your middleware.
        self.get_response = get_response

    def __call__(self, request): #This method runs for every incoming HTTP request.
        if request.user.is_authenticated: #if user login
            request.institution = getattr(request.user, 'institution', None) #attach insitute Get the institution attribute from request.user. If it doesn't exist, return None.
        else:
            request.institution = None
            
        response = self.get_response(request)
        return response

'''
                REQUEST

                   │
                   ▼

        AuthenticationMiddleware
                   │
                   ▼

        request.user is created
                   │
                   ▼

           TenantMiddleware
                   │
                   ▼

     request.institution is added
                   │
                   ▼

                VIEW
                   │
                   ▼

      Patient.objects.filter(
        institution=request.institution
      )
                   │
                   ▼

                RESPONSE
'''