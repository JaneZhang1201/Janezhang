from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path

from .github import GitHubError, github_username, sync_repos
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    change_list_template = "admin/projects/project/change_list.html"
    list_display = ["title", "is_visible", "is_featured", "order", "language", "stars", "last_pushed_at"]
    list_editable = ["is_visible", "is_featured", "order"]
    list_filter = ["is_visible", "is_featured", "language"]
    search_fields = ["title", "summary", "topics"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["stars", "last_pushed_at"]
    fieldsets = [
        (None, {"fields": ["title", "slug", "summary", "body", "image"]}),
        ("On the site", {"fields": ["is_visible", "is_featured", "order"]}),
        ("From GitHub", {"fields": ["repo_url", "homepage_url", "language", "topics", "stars", "last_pushed_at"]}),
    ]

    def get_urls(self):
        custom = [
            path(
                "import-github/",
                self.admin_site.admin_view(self.import_github),
                name="projects_project_import_github",
            ),
        ]
        return custom + super().get_urls()

    def import_github(self, request):
        if request.method != "POST" or not self.has_add_permission(request):
            return redirect("admin:projects_project_changelist")
        username = github_username()
        if not username:
            self.message_user(request, "Add your GitHub URL to your Profile first.", messages.ERROR)
        else:
            try:
                result = sync_repos(username)
            except GitHubError as error:
                self.message_user(request, str(error), messages.ERROR)
            else:
                text = f"Imported from GitHub ({username}): {result.created} new, {result.updated} updated."
                if result.created:
                    text += " New projects are hidden — tick “show on site” to publish them."
                self.message_user(request, text, messages.SUCCESS)
        return redirect("admin:projects_project_changelist")
