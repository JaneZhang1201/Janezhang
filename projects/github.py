"""Import public repositories from GitHub into Project records."""

import json
import os
import re
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.utils.dateparse import parse_datetime
from django.utils.text import slugify

from cv.models import Profile

from .models import Project

API_URL = "https://api.github.com/users/{username}/repos?per_page=100&type=owner&sort=pushed"


class GitHubError(Exception):
    pass


@dataclass
class SyncResult:
    created: int = 0
    updated: int = 0
    skipped_forks: int = 0


def github_username():
    """Use GITHUB_USERNAME if set, otherwise the username in the profile's GitHub URL."""
    if os.environ.get("GITHUB_USERNAME"):
        return os.environ["GITHUB_USERNAME"]
    profile = Profile.objects.first()
    if profile and profile.github_url:
        match = re.match(r"https?://(?:www\.)?github\.com/([^/?#]+)", profile.github_url)
        if match:
            return match.group(1)
    return None


def fetch_repos(username):
    request = Request(API_URL.format(username=username), headers={"Accept": "application/vnd.github+json"})
    # Optional: a token raises GitHub's rate limit from 60 to 5,000 requests an hour.
    if os.environ.get("GITHUB_TOKEN"):
        request.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    try:
        with urlopen(request, timeout=10) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code == 404:
            raise GitHubError(f"GitHub user '{username}' was not found.") from error
        raise GitHubError(f"GitHub returned an error ({error.code}). Try again later.") from error
    except (URLError, TimeoutError) as error:
        raise GitHubError("Couldn't reach GitHub. Check your internet connection.") from error


def unique_slug(name):
    base = slugify(name)[:140] or "project"
    slug, n = base, 2
    while Project.objects.filter(slug=slug).exists():
        slug, n = f"{base}-{n}", n + 1
    return slug


def sync_repos(username, include_forks=False):
    """
    Create a hidden Project for each new repo and refresh GitHub details on existing ones.
    Your own title, summary, write-up and visibility choices are never overwritten.
    """
    result = SyncResult()
    for repo in fetch_repos(username):
        if repo.get("fork") and not include_forks:
            result.skipped_forks += 1
            continue

        github_fields = {
            "repo_url": repo["html_url"],
            "homepage_url": repo.get("homepage") or "",
            "language": repo.get("language") or "",
            "topics": ", ".join(repo.get("topics") or []),
            "stars": repo.get("stargazers_count") or 0,
            "last_pushed_at": parse_datetime(repo["pushed_at"]) if repo.get("pushed_at") else None,
        }
        project = Project.objects.filter(github_id=repo["id"]).first()
        if project is None:
            Project.objects.create(
                github_id=repo["id"],
                title=repo["name"].replace("-", " ").replace("_", " "),
                slug=unique_slug(repo["name"]),
                summary=(repo.get("description") or "").strip()[:300],
                **github_fields,
            )
            result.created += 1
        else:
            for field, value in github_fields.items():
                setattr(project, field, value)
            if not project.summary and repo.get("description"):
                project.summary = repo["description"].strip()[:300]
            project.save()
            result.updated += 1
    return result
