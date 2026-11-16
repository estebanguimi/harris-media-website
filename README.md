# Harris Media Group — sitio web + panel de administración

El sitio web completo de Harris Media Group y un panel sencillo (tipo WordPress) para editarlo sin programar.

- **La web:** portada, Our Clients (con las 15 páginas de clientes), Our Services, Our Works, Our Team (con un perfil por persona), Careers, News y Contact.
- **El panel (`/admin`):** subir fotos y videos a **Our Works**, incluidos enlaces de YouTube, Vimeo, Facebook e Instagram. También escribir y publicar **News** y crear o editar perfiles de **Our Team**.

## Cómo usarlo

👉 **Instrucciones paso a paso en [LEEME.md](LEEME.md)**: cómo abrirlo en tu computadora, cómo se usa el panel, copias de seguridad y cómo ponerlo en internet.

Inicio rápido:

| Sistema | Qué hacer |
|---|---|
| Windows | Instala Python 3.11 o más reciente y haz doble clic en `Iniciar (Windows).bat` |
| Mac | Haz doble clic en `Iniciar (Mac).command` |
| Servidor | `docker build -t hmg-web .` y luego `docker run -d -p 8000:8000 -v hmg-datos:/datos hmg-web` |

La web queda en `http://localhost:8000/` y el panel en `http://localhost:8000/admin`.

## Estructura

| Carpeta | Contenido |
|---|---|
| `app.py`, `templates/`, `static/` | El panel de administración (Flask). |
| `generador/` | El código que construye la web: diseño, animaciones y páginas. El panel lo ejecuta al pulsar «Publicar cambios». |
| `generador/landing/index.html` | La portada, ya construida. |
| `desarrollo/portada/` | Solo para cambiar el diseño de la portada: `reconstruir_portada.sh` la regenera desde `portada-original.html` (necesita Node.js). |
| `contenido/` *(no está en el repositorio)* | Lo que se crea desde el panel: textos, fotos, videos y usuarios. Se genera sola la primera vez y **no se sube a GitHub** porque contiene las contraseñas. |
