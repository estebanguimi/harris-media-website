# Panel de administración — Harris Media Group

Un panel sencillo, tipo WordPress pero mucho más simple, para cambiar la web **sin programar**.

Desde el panel puedes:

| Sección | Qué puedes hacer |
|---|---|
| **Our Works** | Subir trabajos con foto y/o video (archivo MP4 o enlace de YouTube/Vimeo), editarlos, ocultarlos, borrarlos y cambiar el orden. |
| **News** | Escribir noticias nuevas con un editor de texto (subtítulos, negritas, listas, citas, enlaces e imágenes), editarlas, dejarlas en borrador o publicarlas. |
| **Our Team** | Crear o editar el perfil de cada persona: foto, cargo, área, idiomas y biografía (en inglés, español y/o portugués). Cada persona tiene su propia página. |

Todo lo demás de la web (portada, clientes, servicios, etc.) se queda como está.

---

## 1. Abrirlo en tu computadora

1. Instala **Python 3.11 o más reciente** (gratis) desde https://www.python.org/downloads/
   En Windows, en el instalador **marca la casilla “Add Python to PATH”**.
2. Abre esta carpeta y haz doble clic en:
   - Windows → **`Iniciar (Windows).bat`**
   - Mac → **`Iniciar (Mac).command`** (la primera vez: clic derecho → Abrir)
3. Se abre el navegador en **http://localhost:8000/admin**. La primera vez tarda un poco más.
4. La primera vez te pide **crear tu usuario y contraseña**. Después siempre entrarás con ellos.

Mientras la ventana negra esté abierta, el panel funciona. Para apagarlo, cierra esa ventana.

La web completa se ve en **http://localhost:8000/**.

## 2. Cómo se usa

1. Entra a **Our Works**, **News** u **Our Team** en el menú de la izquierda.
2. Pulsa **＋ Subir trabajo / Escribir noticia / Añadir persona**, o **Editar** en uno que ya exista.
3. Rellena el formulario y pulsa **Guardar**.
   - **Guardar y ver vista previa** te enseña cómo quedará la página antes de publicarla (solo la ves tú).
   - **Borrador** = guardado pero oculto. **Publicado** = aparecerá en la web.
4. Cuando termines, pulsa **Publicar cambios** (arriba a la derecha). Ese botón se pone naranja cuando hay cambios pendientes.

Consejos:
- **Videos largos** → súbelos a YouTube o Vimeo y pega el enlace. Los archivos MP4 pueden pesar hasta 400 MB.
- **Fotos** → JPG o PNG normales; el panel las optimiza solo.
- **Texto de noticias** → puedes pegarlo desde Word o Google Docs; se limpia automáticamente.
- **Orden** → en Our Works y Our Team usa las flechas; ese orden es el de la web.
- La noticia con **la fecha más reciente** sale como principal en la página de News.

## 3. Dar acceso a otra persona

En **Mi cuenta** (abajo a la izquierda) puedes crear usuarios para tus compañeros y cambiar tu contraseña.

## 4. Copias de seguridad

Todo lo que creas en el panel se guarda en la carpeta **`contenido/`** (textos + fotos y videos).
Para tener una copia de seguridad, **copia esa carpeta** a otro lugar (Drive, disco externo…).

## 5. Ponerlo en internet (lo hace una sola vez alguien técnico)

El panel y la web van juntos en un único programa. Para que esté online, hay que instalarlo una vez en un servidor:

- **Con Docker** (recomendado):
  ```
  docker build -t hmg-panel .
  docker run -d -p 8000:8000 -v hmg-datos:/datos --restart unless-stopped hmg-panel
  ```
  El volumen `/datos` guarda el contenido y la web publicada: **no lo borres**.
- **Sin Docker:** `pip install -r requirements.txt` y `HOST=0.0.0.0 PORT=8000 python app.py`.
- Pon delante un proxy con **HTTPS** (Nginx, Caddy, Cloudflare…) que apunte al puerto 8000, y define la variable `HMG_HTTPS=1`.
- La web pública queda en `/` y el panel en `/admin`.

Variables opcionales: `HMG_DATA` (carpeta del contenido), `HMG_PUBLIC` (carpeta de la web publicada), `PORT`, `HOST`.

## 6. Qué hay en cada carpeta

| Carpeta / archivo | Qué es |
|---|---|
| `app.py` | El panel. |
| `templates/`, `static/` | Las pantallas del panel. |
| `generador/` | El código que construye la web (diseño, animaciones, páginas de clientes…). |
| `contenido/` | **Tu contenido** (se crea solo la primera vez). Haz copias de esta carpeta. |
| `sitio-publicado/` | La web tal como se ve en internet (se rehace al pulsar «Publicar cambios»). |
