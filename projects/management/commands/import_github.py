from django.core.management.base import BaseCommand, CommandError

from projects.github import GitHubError, github_username, sync_repos


class Command(BaseCommand):
    help = "Import your public GitHub repositories as (hidden) projects, and refresh existing ones."

    def add_arguments(self, parser):
        parser.add_argument("username", nargs="?", help="GitHub username (defaults to the one in your profile)")
        parser.add_argument("--include-forks", action="store_true")

    def handle(self, *args, username=None, include_forks=False, **options):
        username = username or github_username()
        if not username:
            raise CommandError("No GitHub username: pass one, or add your GitHub URL to your profile.")
        try:
            result = sync_repos(username, include_forks=include_forks)
        except GitHubError as error:
            raise CommandError(str(error)) from error
        self.stdout.write(self.style.SUCCESS(
            f"{username}: {result.created} new, {result.updated} updated, {result.skipped_forks} forks skipped."
        ))
        if result.created:
            self.stdout.write("New projects are hidden — tick 'show on site' in the admin to publish them.")
