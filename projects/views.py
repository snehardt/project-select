from django.db.models import Q
from django.contrib.staticfiles import finders
from django.shortcuts import get_object_or_404, render
from .forms import ProjectSearchForm
from .models import Project

def index(request):
    form = ProjectSearchForm(request.GET)
    projects = Project.objects.filter(published=True)
    total = projects.count()
    query = ""
    valid = form.is_valid()
    if valid:
        query = form.cleaned_data["q"]
        if query:
            projects = projects.filter(
                Q(title__icontains=query) | Q(summary__icontains=query) | Q(technologies__icontains=query)
            )
    else:
        projects = projects.none()
    return render(request, "projects/index.html", {
        "projects": projects, "form": form, "query": query, "total": total, "search_valid": valid,
    })

def detail(request, slug):
    project = get_object_or_404(Project.objects.prefetch_related("screenshots"), slug=slug, published=True)
    collection = list(Project.objects.filter(published=True))
    position = next(i for i, item in enumerate(collection) if item.pk == project.pk)
    next_project = collection[(position + 1) % len(collection)] if len(collection) > 1 else None
    download_asset = f"projects/downloads/{project.slug}-windows.zip"
    if not finders.find(download_asset):
        download_asset = None
    return render(request, "projects/detail.html", {
        "project": project, "next_project": next_project, "download_asset": download_asset,
    })
