from .models import Profile


def site_profile(request):
    """Make the owner's profile available to every template (navbar, footer, page titles)."""
    return {"site_profile": Profile.objects.first()}
