# Harris Media Group — website + admin panel

The complete Harris Media Group website and a simple admin panel (WordPress-style, but much simpler) to update it without any coding.

- **Website:** homepage, Our Clients (with 15 client pages), Our Services, Our Works, Our Team (one profile per person), Careers, News and Contact.
- **Admin panel (`/admin`):** add photos, videos and links (YouTube, Vimeo, Facebook, Instagram) to **Our Works**, write and publish **News**, and create or edit **Our Team** profiles.

## How to use it

👉 **Step-by-step instructions in [GUIDE.md](GUIDE.md)**: running it on your computer, using the panel, backups and putting it online.

Quick start:

| Where | What to do |
|---|---|
| Windows | Install Python 3.11 or newer and double-click `Start (Windows).bat` |
| Mac | Double-click `Start (Mac).command` |
| **Online (free)** | Follow [deploy/PYTHONANYWHERE.md](deploy/PYTHONANYWHERE.md): website + panel on your own link |
| Your own server | `docker build -t hmg-web .` then `docker run -d -p 8000:8000 -v hmg-data:/data hmg-web` |

The website runs at `http://localhost:8000/` and the panel at `http://localhost:8000/admin` (or the small lock next to the © in the footer).

## Structure

| Folder | Contents |
|---|---|
| `app.py`, `templates/`, `static/` | The admin panel (Flask). |
| `generator/` | The code that builds the website: design, animations and pages. The panel runs it when you press "Publish changes". |
| `generator/landing/index.html` | The homepage, already built. |
| `deploy/` | One-command installer for PythonAnywhere. |
| `development/homepage/` | Only to change the homepage design: `rebuild_homepage.sh` rebuilds it from `homepage-original.html` (requires Node.js). |
| `content/` *(not in the repository)* | Everything created in the panel: texts, photos, videos and users. Created automatically on first start and **never uploaded to GitHub** because it contains the passwords. |
