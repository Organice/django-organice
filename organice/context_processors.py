"""django Organice processor for TEMPLATE_CONTEXT_PROCESSORS settings"""
from django.contrib.sites.models import Site


def expose(request):
    """Expose specific objects or values to the project templates"""
    return {'current_site': Site.objects.get_current()}
