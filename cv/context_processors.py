from .models import Profile


def site_profile(request):
    """Make the owner's profile and current nav section available to every template."""
    match = getattr(request, "resolver_match", None)  # None on 404 pages
    section = (match.namespace or match.url_name) if match else ""
    return {"site_profile": Profile.objects.first(), "nav_section": section}
