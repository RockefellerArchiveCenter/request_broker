from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from process_request.models import User

if all([
        getattr(settings, 'DJANGO_SUPERUSER_USERNAME', None),
        getattr(settings, 'DJANGO_SUPERUSER_PASSWORD', None),
        getattr(settings, 'DJANGO_SUPERUSER_EMAIL', None)]):
    if not User.objects.filter(username=settings.DJANGO_SUPERUSER_USERNAME).exists():
        User.objects.create_superuser(
            username=settings.DJANGO_SUPERUSER_USERNAME,
            password=settings.DJANGO_SUPERUSER_PASSWORD,
            email=settings.DJANGO_SUPERUSER_EMAIL,
            is_staff=True)
else:
    raise ImproperlyConfigured("Values for DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_PASSWORD and DJANGO_SUPERUSER_EMAIL must be set in config.py")
