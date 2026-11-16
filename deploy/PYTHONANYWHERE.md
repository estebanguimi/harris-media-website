# Putting the website + panel online with PythonAnywhere (free)

This gives you the website **and the panel** working on your own link:

- Website: `https://YOUR-USERNAME.pythonanywhere.com/`
- Panel: `https://YOUR-USERNAME.pythonanywhere.com/admin` (or the lock next to the © in the footer)

Everything you add in the panel (photos, stories, profiles, users) **is kept**.

## Steps (about 10 minutes)

1. **Create a free account** at https://www.pythonanywhere.com → *Pricing & signup* → **Create a Beginner account**.
   The username you choose becomes part of the link.

2. **Create the web app.** **Web** tab → **Add a new web app** → *Next* → **Manual configuration** → **Python 3.11** → *Next*.

3. **Install the panel.** **Consoles** tab → **Bash**. In the black screen that opens, paste this and press Enter:

   ```
   git clone https://github.com/estebanguimi/harris-media-website.git && bash harris-media-website/deploy/pythonanywhere.sh
   ```

   It takes 1–2 minutes and ends with **"Done!"** and your links.

4. **Turn it on.** Go back to the **Web** tab and press the green **Reload** button.

5. Open `https://YOUR-USERNAME.pythonanywhere.com/admin` and **create your username and password**.

## To update it when the code changes

In **Consoles → Bash**, paste the following and then press **Reload** in the Web tab:

```
bash harris-media-website/deploy/pythonanywhere.sh
```

Your content is not deleted when updating.

## Free account limits

- **512 MB of storage.** For videos use YouTube, Vimeo, Facebook or Instagram links instead of uploading MP4 files.
- **Every 3 months** PythonAnywhere asks you to log in and press **"Run until 3 months from today"** in the Web tab. If you don't, the website is paused (nothing is deleted).
- The link is `YOUR-USERNAME.pythonanywhere.com`. A custom domain requires a paid plan.
