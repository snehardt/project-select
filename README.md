# Project Select

A Django portfolio by Spencer Ehardt. A dark, text-first index introduces five projects; each has its own URL with development notes, technology, links, and an initially collapsed screenshot gallery. The selection-frame logo is also used as the favicon and footer mark.

**Live website:** https://spencerehardt.pythonanywhere.com/

## Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py seed_projects
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000. The server must stay running while using the site.

On macOS/Linux, use `.venv/bin/python` in place of `.\.venv\Scripts\python.exe`.

## Edit projects

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Choose your own username and password, then sign in at http://127.0.0.1:8000/admin/. Add/edit projects, reorder them, or hide them with the Published checkbox. Separate technologies with commas; put each current feature or next step on a new line. Screenshots reference files in `static/`, e.g. `projects/images/snake.png`. Add the file there, then add its relative path and caption in the project's admin page.

`seed_projects` adds missing starter records without replacing project edits. The database is local and ignored by Git; back it up to preserve edits. Re-running the seed command also restores missing starter screenshot records.

## Contact information

The owner's email hasn't been supplied. The footer currently links to GitHub rather than displaying a made-up address. Set the email before starting the server:

```powershell
$env:SITE_CONTACT_EMAIL = 'your-real-email@example.com'
```

The footer displays the email link once configured. Django does not automatically read `.env` files; set variables in your terminal or hosting provider.

## Assignment requirements

| Requirement | Implementation |
| --- | --- |
| Server-generated HTML | Django views render the index and five project detail pages. |
| Local CSS/images | `static/projects/` includes CSS, SVG branding, and real project preview images. |
| User input | A GET search form accepts a project name or technology. |
| Input validation | `ProjectSearchForm` checks a maximum of 80 characters and rejects control characters on the server. |
| HTML changes based on input | The server queries projects and renders matches, a result count, errors, or an empty state. |
| Database stretch | SQLite stores editable projects and screenshot metadata using Django models and migrations. |

## How it fits together

- `config/`: settings and the root URL routes.
- `projects/models.py`: database structure for projects and screenshots.
- `projects/views.py`: handles search and project detail requests.
- `projects/forms.py`: validates visitor input.
- `templates/`: shared HTML and page templates.
- `static/projects/`: styling, gallery enhancement, branding, and preview images.
- `projects/management/commands/seed_projects.py`: initial collection based on the original projects' READMEs.

The gallery and instruction disclosures use native HTML `<details>`. Search and navigation work without JavaScript. JavaScript only enhances the Screenshots shortcut. Pages support keyboard navigation, visible focus, small screens, and reduced motion.

## Checks

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
.\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

## Hosting later

For step-by-step instructions tailored to this repository, see [HOSTING.md](HOSTING.md).
Source repository: https://github.com/snehardt/project-select

This app runs on PythonAnywhere at https://spencerehardt.pythonanywhere.com/.
GitHub Pages cannot run Django. See HOSTING.md for the deployed configuration and update steps.

For deployment, set `DJANGO_DEBUG=false`, a long random `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` (comma-separated hostnames), and optionally `SITE_CONTACT_EMAIL`. Apply migrations and run `collectstatic`. WhiteNoise serves the collected CSS and images. Use a persistent disk for `db.sqlite3` (or configure a managed database before hosting on ephemeral storage). Run with an HTTPS reverse proxy and a production WSGI server, such as:

```powershell
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8000 config.wsgi:application
```

The host must provide HTTPS. Configure trusted proxy HTTPS headers only according to that provider's documented proxy setup, then run `manage.py check --deploy`. The development server is for local use.

## Content notes

- The Hazardous Lies game and repository links were taken from local project documentation; external availability may change.
- Blockwood has no public URL recorded in the local project; its page provides local run instructions.
- Parachute's current version sends animation commands. Actual file sharing is planned. Team members are credited, and the code contribution breakdown still needs the owner's review.
- Dungeon Descent's final floor boss is still planned.
- Preview images come from the existing projects or local captures. They are demonstrations of development builds, not promises that every feature is finished.

Game pages support a hosted play link (`demo_url`) and an optional packaged download or shared-folder link (`download_url`), both editable in admin. Leave optional descriptions, limitations, and controls blank to hide those sections.

Snake includes a Windows x64 download at `static/projects/downloads/snake-windows.zip`.
Its page automatically shows "Download for Windows" when this file is present,
with extraction instructions. Python is included in the download. To rebuild it
from the neighboring game project, run its `build_windows.py --portfolio ../Portfolio`
using the build environment described in `../Sprint1_Game/README.md`, then run
`collectstatic` again before deployment. Packaged downloads follow the convention
`static/projects/downloads/<project-slug>-windows.zip` and take priority over
the project's external download link. Dungeon Descent has no packaged download.
