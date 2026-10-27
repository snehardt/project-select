from django.conf import settings

def identity(request):
    return {"contact_email": settings.SITE_CONTACT_EMAIL}
