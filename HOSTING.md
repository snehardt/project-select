# Put Project Select online with PythonAnywhere

Repository: https://github.com/snehardt/project-select

The repository shares the source. PythonAnywhere runs Django and gives you a
public website address. GitHub Pages cannot run this Django application.

## Current deployment

Deployed October 27, 2026:

- Public URL: https://spencerehardt.pythonanywhere.com/
- PythonAnywhere username: `spencerehardt`
- Project: `/home/spencerehardt/project-select`
- Python: 3.13; virtualenv: `/home/spencerehardt/.virtualenvs/project-select`
- Static mapping: `/static/` to `/home/spencerehardt/project-select/staticfiles`
- Host WSGI file: `/var/www/spencerehardt_pythonanywhere_com_wsgi.py`
- The WSGI file sets `DJANGO_DEBUG=false`, the allowed hostname, and the settings
  module. It generates a stable private key in `/home/spencerehardt/.project-select-secret`
  with owner-only permissions and reads it on subsequent reloads. Keep that file
  private and backed up; do not put it in Git. This deployment does not use `.env`.
- Force HTTPS is enabled. The database is SQLite on the host's persistent storage.
- An admin user has not been created by the deployment workflow. Create one only
  if you want to edit project records through `/admin/`.

**Free-site renewal:** log in monthly, open the Web tab, and click
**Run until 1 month from today**. The initial expiry shown was November 27, 2026.
Use the current expiry on the Web tab as the source of truth.

### Update this deployed site

Push local changes to GitHub, then run these commands in the PythonAnywhere Bash
console. Wait for each command to finish before running the next:

```bash
workon project-select
cd ~/project-select
git pull --ff-only
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **Reload spencerehardt.pythonanywhere.com** on the Web tab. The install
step is needed when dependencies change; migrate is needed when database models
change; collectstatic is needed when assets or the Snake ZIP change. Admin content
edits take effect when saved. `seed_projects` adds missing starter projects but
preserves existing records, so it does not overwrite admin edits.

The remaining guide describes setting up a **new** deployment using an `.env`
file as an alternative to the current WSGI-managed private key.

## 1. Create your hosting account

Sign up at https://www.pythonanywhere.com/ and open **Consoles > Bash**.
Use your PythonAnywhere username wherever `YOUR_USERNAME` appears below.
Use the actual hostname shown on your Web tab if it differs from the example.
Check the current account limits and renewal requirements for your chosen plan.

## 2. Download the site and install dependencies

Run these commands in the PythonAnywhere Bash console, not your Windows terminal:

```bash
git clone https://github.com/snehardt/project-select.git
cd ~/project-select
mkvirtualenv --python=/usr/bin/python3.13 project-select
pip install -r requirements.txt
pip install python-dotenv
```

If Python 3.13 is unavailable, use an available Python 3.10 or newer version;
select that same version when creating the web app in step 4.

## 3. Create production configuration and initialize the site

This creates a private `.env` file on the host. It generates a random secret key
and prompts for your website hostname. Enter just the hostname, without `https://`
or a trailing slash (for example `YOUR_USERNAME.pythonanywhere.com`).

```bash
read -r -p 'Website hostname: ' PROJECT_SELECT_HOST
export PROJECT_SELECT_HOST
python - <<'PY'
from pathlib import Path
import os
import secrets

config_path = Path('.env')
if config_path.exists():
    raise SystemExit('.env already exists; keep it and continue with the next commands.')
hostname = os.environ['PROJECT_SELECT_HOST'].strip()
if not hostname or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-' for c in hostname):
    raise SystemExit('Enter a hostname only, without https:// or slashes.')
config_path.write_text(
    'DJANGO_DEBUG=false\n'
    f'DJANGO_SECRET_KEY={secrets.token_urlsafe(64)}\n'
    f'DJANGO_ALLOWED_HOSTS={hostname}\n'
)
config_path.chmod(0o600)
print('Created private production configuration.')
PY
set -a
source .env
set +a
python manage.py migrate
python manage.py seed_projects
python manage.py collectstatic --noinput
python manage.py check --deploy
```

The deployment check may suggest longer HSTS settings, subdomain coverage, or
preloading. Those are deliberate policy choices; do not enable subdomain coverage
or preloading for a shared hosting domain. Debug must be off and the secret must
be private. `.env` and the database are already ignored by Git.

Optional: run `python manage.py createsuperuser` to edit projects at `/admin/`.
To show an email link, add `SITE_CONTACT_EMAIL=your-address` to `.env`.

## 4. Create the web app

Open **Web > Add a new web app > Manual configuration** and choose the Python
version used in step 2. Use Manual configuration because this project already exists.

Set:

- **Source code / Working directory:** `/home/YOUR_USERNAME/project-select`
- **Virtualenv:** `/home/YOUR_USERNAME/.virtualenvs/project-select`

Open the **WSGI configuration file** linked on the Web tab. Replace its sample
contents with this (this is the host's WSGI file, not `config/wsgi.py` in the repo):

```python
import os
import sys
from dotenv import load_dotenv

project_path = '/home/YOUR_USERNAME/project-select'
sys.path.insert(0, project_path)
load_dotenv(os.path.join(project_path, '.env'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `YOUR_USERNAME`, then save.

## 5. Connect static files and enable HTTPS

Under **Web > Static files**, add:

| URL | Directory |
| --- | --- |
| `/static/` | `/home/YOUR_USERNAME/project-select/staticfiles` |

Under **Security**, enable **Force HTTPS**. PythonAnywhere supplies HTTPS for its
own website subdomains. Click **Reload** near the top of the Web tab.

Open `https://YOUR_USERNAME.pythonanywhere.com/`. Share this address with visitors.
Test search, screenshots, and the Snake Windows download before sharing it.
The ZIP is included in the repository and is collected with the other static files.

If there is an error, open the **error log** linked on the Web tab. Check the
username/path, virtualenv, hostname in `.env`, and Python version first. If you
see repeated HTTPS redirects, check the host's HTTPS/proxy configuration before
changing Django's security settings.

## Publish later updates

After pushing changes to GitHub, run in a PythonAnywhere Bash console:

```bash
workon project-select
cd ~/project-select
set -a
source .env
set +a
git pull --ff-only
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_projects
python manage.py collectstatic --noinput
```

Then click **Reload** on the Web tab. Existing admin edits survive `seed_projects`;
edit existing project text through admin when needed. Back up `db.sqlite3` before
major changes; it holds the live project edits and admin account.

## Official references

- [Deploy an existing Django project](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Load environment variables](https://help.pythonanywhere.com/pages/EnvironmentVariables/)
- [Configure static files](https://help.pythonanywhere.com/pages/DjangoStaticFiles/)
- [Force HTTPS](https://help.pythonanywhere.com/pages/ForcingHTTPS)
