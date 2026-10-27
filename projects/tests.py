from io import StringIO
from unittest.mock import patch
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Project


@override_settings(STORAGES={"staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
class PortfolioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_projects", stdout=StringIO())

    def test_index_has_real_projects_without_preview_images(self):
        response = self.client.get(reverse("projects:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dungeon Descent")
        self.assertContains(response, "Blockwood")
        self.assertNotContains(response, "projects/images/")
        self.assertEqual(len(response.context["projects"]), 5)

    def test_search_filters_server_rendered_projects(self):
        response = self.client.get("/", {"q": "Python"})
        self.assertEqual({p.slug for p in response.context["projects"]}, {"snake", "dungeon-descent"})
        self.assertNotContains(response, "Hazardous Lies")

    def test_no_results_and_whitespace(self):
        self.assertContains(self.client.get("/", {"q": "does-not-exist"}), "No projects found.")
        response = self.client.get("/", {"q": "   "})
        self.assertEqual(len(response.context["projects"]), 5)

    def test_invalid_input_rejected_by_server(self):
        for query in ("x" * 81, "hello\x00there"):
            response = self.client.get("/", {"q": query})
            self.assertTrue(response.context["form"].errors)
            self.assertEqual(len(response.context["projects"]), 0)
            self.assertContains(response, 'role="alert"')

    def test_input_is_escaped(self):
        response = self.client.get("/", {"q": '<script>alert("x")</script>'})
        self.assertNotContains(response, '<script>alert("x")</script>')
        self.assertContains(response, "&lt;script&gt;")

    def test_detail_pages_and_collapsed_gallery(self):
        for project in Project.objects.all():
            response = self.client.get(project.get_absolute_url())
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, project.title)
            self.assertContains(response, "Where it's at")
            self.assertContains(response, "Where it is")
            self.assertContains(response, "Future progress")
            for removed in ("The idea", "Good to know", "How to play / use", "Run it locally"):
                self.assertNotContains(response, removed)
            self.assertContains(response, 'id="screenshots"')
            self.assertNotContains(response, 'id="screenshots" open')

    def test_unpublished_and_unknown_projects_are_not_public(self):
        project = Project.objects.get(slug="snake")
        project.published = False
        project.save()
        self.assertNotContains(self.client.get("/"), "Snake")
        self.assertEqual(self.client.get(project.get_absolute_url()).status_code, 404)
        self.assertEqual(self.client.get("/projects/missing/").status_code, 404)

    def test_seed_keeps_admin_edits(self):
        project = Project.objects.get(slug="snake")
        project.summary = "My updated description"
        project.save()
        call_command("seed_projects", stdout=StringIO())
        project.refresh_from_db()
        self.assertEqual(project.summary, "My updated description")
        self.assertEqual(Project.objects.count(), 5)

    def test_admin_requires_login(self):
        response = self.client.get("/admin/")
        self.assertRedirects(response, "/admin/login/?next=/admin/")

    @override_settings(SITE_CONTACT_EMAIL="spencer@example.com")
    def test_contact_email_is_configurable(self):
        self.assertContains(self.client.get("/"), "mailto:spencer@example.com")

    def test_hazardous_lies_content_and_play_link(self):
        project = Project.objects.get(slug="hazardous-lies")
        response = self.client.get(project.get_absolute_url())
        for text in ("Playable prototype", "Where it is", "10 levels", "Future progress", "My role", "independently"):
            self.assertContains(response, text)
        for text in ("The idea", "Good to know", "How to play / use"):
            self.assertNotContains(response, text)
        self.assertContains(response, f'href="{project.demo_url}"')
        self.assertNotContains(response, "Download to play")

    def test_optional_game_download_link(self):
        project = Project.objects.get(slug="hazardous-lies")
        project.download_url = "https://example.com/releases/game.zip"
        project.save()
        response = self.client.get(project.get_absolute_url())
        self.assertContains(response, 'href="https://example.com/releases/game.zip"')
        self.assertContains(response, "Download to play")

    def test_every_seeded_project_has_access_screenshots_and_source(self):
        for project in Project.objects.all():
            with self.subTest(project=project.slug):
                self.assertTrue(project.source_url)
                if project.slug in ("dungeon-descent", "snake"):
                    self.assertFalse(project.demo_url or project.download_url)
                    self.assertNotContains(response := self.client.get(project.get_absolute_url()), "Download to play")
                else:
                    self.assertTrue(project.demo_url or project.download_url)
                response = self.client.get(project.get_absolute_url())
                self.assertContains(response, f'href="{project.source_url}"')
                if project.demo_url or project.download_url:
                    self.assertContains(response, f'href="{project.demo_url or project.download_url}"')
                self.assertContains(response, 'href="#screenshots"')
                self.assertContains(response, "View code")
                if project.download_url and not project.demo_url:
                    self.assertContains(response, "Python required")
                    self.assertContains(response, project.run_instructions.splitlines()[-1])

    def test_header_brand_only_appears_on_project_pages(self):
        self.assertNotContains(self.client.get(reverse("projects:index")), 'class="brand"')
        for project in Project.objects.all():
            self.assertContains(self.client.get(project.get_absolute_url()), 'class="brand"')

    def test_snake_windows_download_and_instructions(self):
        response = self.client.get("/projects/snake/")
        self.assertContains(response, 'href="/static/projects/downloads/snake-windows.zip" download')
        self.assertContains(response, "Download for Windows")
        self.assertContains(response, "No Python installation is needed")
        self.assertNotContains(response, "Python required")
        self.assertNotContains(self.client.get("/projects/dungeon-descent/"), "Download for Windows")

    @patch("projects.views.finders.find", return_value=None)
    def test_missing_package_has_no_broken_download_button(self, find_asset):
        response = self.client.get("/projects/snake/")
        self.assertNotContains(response, "Download for Windows")
        self.assertNotContains(response, "How to play on Windows")
