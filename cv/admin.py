from django.contrib import admin

from .models import Education, Experience, Profile, Skill


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["name", "headline", "email", "has_cv_pdf"]
    fieldsets = [
        (None, {"fields": ["name", "headline", "intro", "photo"]}),
        ("CV", {"fields": ["cv_file", "summary", "hobbies"]}),
        ("Contact & links", {"fields": ["email", "location", "github_url", "linkedin_url"]}),
    ]

    @admin.display(boolean=True, description="CV PDF")
    def has_cv_pdf(self, obj):
        return bool(obj.cv_file)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ["role", "organisation", "start_date", "end_date"]


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["qualification", "subject", "institution", "end_year"]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]
