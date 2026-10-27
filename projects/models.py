from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse

web_url = URLValidator(schemes=["http", "https"])


class Project(models.Model):
    class Category(models.TextChoices):
        GAME = "game", "Game"
        WEB = "web", "Web application"
        TOOL = "tool", "Tool"

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=240)
    category = models.CharField(max_length=12, choices=Category, default=Category.GAME)
    status = models.CharField(max_length=60, default="In development")
    technologies = models.CharField(max_length=200, help_text="Separate technologies with commas.")
    description = models.TextField(blank=True)
    works_today = models.TextField("where it is", help_text="One feature per line.")
    next_steps = models.TextField("future progress", help_text="One planned improvement per line.")
    limitations = models.TextField(blank=True)
    contribution = models.TextField("my role", blank=True)
    source_url = models.URLField(blank=True, validators=[web_url])
    demo_url = models.URLField(blank=True, validators=[web_url])
    download_url = models.URLField(blank=True, validators=[web_url], help_text="Link to a packaged game download or shared download folder.")
    demo_label = models.CharField(max_length=40, default="Play in browser")
    controls = models.TextField(blank=True)
    run_instructions = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort_order", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    @property
    def technology_list(self):
        return [value.strip() for value in self.technologies.split(",") if value.strip()]

    @property
    def feature_list(self):
        return self.works_today.splitlines()

    @property
    def next_list(self):
        return self.next_steps.splitlines()


class Screenshot(models.Model):
    project = models.ForeignKey(Project, related_name="screenshots", on_delete=models.CASCADE)
    asset = models.CharField(max_length=250, help_text="Path relative to static/, e.g. projects/images/game.png")
    caption = models.CharField(max_length=240)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "pk"]

    def clean(self):
        super().clean()
        if self.asset.startswith(("/", "\\")) or ".." in self.asset or ":" in self.asset or "\\" in self.asset:
            raise ValidationError({"asset": "Use a relative path inside static/."})

    def __str__(self):
        return self.caption
