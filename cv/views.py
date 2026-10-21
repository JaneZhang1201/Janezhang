from django.shortcuts import render

from blog.models import Post
from projects.models import Project

from .models import Education, Experience, Skill


def home(request):
    return render(
        request,
        "home.html",
        {
            "featured_projects": Project.visible.filter(is_featured=True)[:4],
            "recent_posts": Post.published.all()[:3],
        },
    )


def cv(request):
    return render(
        request,
        "cv/cv.html",
        {
            "experiences": Experience.objects.all(),
            "education": Education.objects.all(),
            "skills": Skill.objects.all(),
            "projects": Project.visible.filter(is_featured=True),
        },
    )
