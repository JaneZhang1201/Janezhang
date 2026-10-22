from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cv.models import Profile

from .github import github_username, sync_repos
from .models import Project


def fake_repo(id, name, **extra):
    return {
        "id": id,
        "name": name,
        "html_url": f"https://github.com/jane/{name}",
        "description": f"About {name}",
        "homepage": "",
        "language": "Python",
        "topics": ["django"],
        "stargazers_count": 3,
        "pushed_at": "2026-01-02T03:04:05Z",
        "fork": False,
        **extra,
    }


@mock.patch("projects.github.fetch_repos")
class SyncReposTests(TestCase):
    def test_new_repos_are_imported_hidden_and_forks_skipped(self, fetch):
        fetch.return_value = [fake_repo(1, "my-app"), fake_repo(2, "someone-elses", fork=True)]
        result = sync_repos("jane")
        self.assertEqual((result.created, result.updated, result.skipped_forks), (1, 0, 1))
        project = Project.objects.get()
        self.assertEqual(project.title, "my app")
        self.assertEqual(project.slug, "my-app")
        self.assertEqual(project.summary, "About my-app")
        self.assertFalse(project.is_visible)

    def test_resync_refreshes_github_fields_but_keeps_your_edits(self, fetch):
        fetch.return_value = [fake_repo(1, "my-app")]
        sync_repos("jane")
        Project.objects.update(title="My App", summary="My own words", is_visible=True)

        fetch.return_value = [fake_repo(1, "my-app", stargazers_count=10, description="New text")]
        result = sync_repos("jane")

        project = Project.objects.get()
        self.assertEqual(result.updated, 1)
        self.assertEqual(project.stars, 10)
        self.assertEqual((project.title, project.summary, project.is_visible), ("My App", "My own words", True))

    def test_slug_clash_gets_a_suffix(self, fetch):
        Project.objects.create(title="Existing", slug="my-app")
        fetch.return_value = [fake_repo(1, "my-app")]
        sync_repos("jane")
        self.assertTrue(Project.objects.filter(slug="my-app-2").exists())


class UsernameTests(TestCase):
    def test_username_comes_from_profile_github_url(self):
        Profile.objects.create(name="Zhaohan", github_url="https://github.com/JaneZhang1201/")
        self.assertEqual(github_username(), "JaneZhang1201")

    def test_no_profile_means_no_username(self):
        self.assertIsNone(github_username())


class ProjectPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.shown = Project.objects.create(title="Shown", slug="shown", is_visible=True, is_featured=True,
                                           repo_url="https://github.com/jane/shown")
        cls.hidden = Project.objects.create(title="Hidden", slug="hidden")

    def test_list_shows_only_visible_projects(self):
        response = self.client.get(reverse("projects:list"))
        self.assertContains(response, "Shown")
        self.assertNotContains(response, "Hidden")

    def test_hidden_project_page_is_404(self):
        self.assertEqual(self.client.get(self.hidden.get_absolute_url()).status_code, 404)

    def test_detail_links_to_repo(self):
        self.assertContains(self.client.get(self.shown.get_absolute_url()), "https://github.com/jane/shown")

    def test_featured_projects_appear_on_home_and_cv(self):
        for name in ("home", "cv"):
            with self.subTest(page=name):
                self.assertContains(self.client.get(reverse(name)), "Shown")


class AdminImportButtonTests(TestCase):
    def setUp(self):
        self.client.force_login(User.objects.create_superuser("admin", "a@example.com", "pw"))
        Profile.objects.create(name="Zhaohan", github_url="https://github.com/zhaohan")

    @mock.patch("projects.github.fetch_repos", return_value=[fake_repo(1, "my-app")])
    def test_import_button_imports_and_reports(self, fetch):
        response = self.client.post(reverse("admin:projects_project_import_github"), follow=True)
        fetch.assert_called_once_with("zhaohan")
        self.assertContains(response, "1 new")
        self.assertContains(response, "Import from GitHub")
        self.assertEqual(Project.objects.count(), 1)
