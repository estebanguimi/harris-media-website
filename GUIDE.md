# Admin panel guide — Harris Media Group

A simple panel, WordPress-style but much simpler, to update the website **without any coding**.

| Section | What you can do |
|---|---|
| **Our Works** | Add works with a photo, an uploaded video, or a link (YouTube, Vimeo, Facebook, Instagram); edit, hide, delete and reorder them. They appear on the Our Works page and in the homepage gallery. |
| **News** | Write new stories with a text editor (subheadings, bold, lists, quotes, links and images), edit them, keep them as drafts or publish them. |
| **Our Team** | Create or edit each person's profile: photo, job title, department, languages and biography (English, Spanish and/or Portuguese). Each person gets their own page. |

The rest of the website (homepage design, clients, services, etc.) stays as it is.

---

## 1. Open the panel

- **Online:** go to `https://YOUR-SITE/admin`, or click the small lock next to the **©** in the footer of any page.
- **On your computer:**
  1. Install **Python 3.11 or newer** (free) from https://www.python.org/downloads/ — on Windows, **tick "Add Python to PATH"** in the installer.
  2. Double-click **`Start (Windows).bat`** or **`Start (Mac).command`** (first time on Mac: right-click → Open).
  3. Your browser opens **http://localhost:8000/admin**. The first start takes a little longer.

The first time the panel is opened it asks you to **create a username and password**.

## 2. How to use it

1. Go to **Our Works**, **News** or **Our Team** in the left menu.
2. Press **＋ Add work / Write a story / Add a person**, or **Edit** on an existing one.
3. Fill in the form and press **Save**.
   - **Save and preview** shows the page exactly as it will look before publishing (only you can see it).
   - **Draft** = saved but hidden. **Published** = will appear on the website.
4. When you are done, press **Publish changes** (top right). The button turns orange when there are pending changes.

Tips:
- **Links:** copy them with **Share → Copy link** or from the browser address bar. The post must be **public**. The website shows the official cover and plays the video inside the frame.
- **Long videos:** upload them to YouTube, Vimeo or Facebook and paste the link. Uploaded MP4 files can be up to 400 MB.
- **Photos:** normal JPG or PNG; the panel optimizes them automatically.
- **News text:** you can paste it from Word or Google Docs; it is cleaned up automatically.
- **Order:** in Our Works and Our Team use the arrows; that order is the order on the website.
- The story with **the most recent date** is the lead story on the News page.

## 3. Give someone else access

In **My account** (bottom left) you can create users for your colleagues and change your password.

## 4. Backups

Everything created in the panel is stored in the **`content/`** folder (texts + photos and videos).
To keep a backup, **copy that folder** somewhere else (Drive, external disk…).

## 5. Putting it online

**Easiest way (free):** follow [deploy/PYTHONANYWHERE.md](deploy/PYTHONANYWHERE.md).

**On your own server** (done once by someone technical):

- **With Docker** (recommended):
  ```
  docker build -t hmg-web .
  docker run -d -p 8000:8000 -v hmg-data:/data --restart unless-stopped hmg-web
  ```
  The `/data` volume keeps the content and the published website: **do not delete it**.
- **Without Docker:** `pip install -r requirements.txt` and `HOST=0.0.0.0 PORT=8000 python app.py`.
- Put an **HTTPS** proxy in front (Nginx, Caddy, Cloudflare…) pointing to port 8000, and set `HMG_HTTPS=1`.
- The public website is at `/` and the panel at `/admin`.

Optional variables: `HMG_DATA` (content folder), `HMG_PUBLIC` (published website folder), `PORT`, `HOST`.

## 6. What is in each folder

| Folder / file | What it is |
|---|---|
| `app.py` | The panel. |
| `templates/`, `static/` | The panel screens. |
| `generator/` | The code that builds the website (design, animations, client pages…). |
| `content/` | **Your content** (created automatically). Back up this folder. |
| `site/` | The website as it is published (rebuilt when you press "Publish changes"). |
