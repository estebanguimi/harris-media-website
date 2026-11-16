# Poner el panel en internet con PythonAnywhere (gratis)

Con esto tendrás la web **y el panel funcionando** en un link propio:

- Web: `https://TU-USUARIO.pythonanywhere.com/`
- Panel: `https://TU-USUARIO.pythonanywhere.com/admin` (o el candado junto al © del pie de página)

Todo lo que subas desde el panel (fotos, noticias, perfiles, usuarios) **se queda guardado**.

## Pasos (unos 10 minutos)

1. **Crea una cuenta gratis** en https://www.pythonanywhere.com → *Pricing & signup* → **Create a Beginner account**.
   El nombre de usuario que elijas formará parte del link.

2. **Crea la web app.** Pestaña **Web** → **Add a new web app** → *Next* → **Manual configuration** → **Python 3.11** → *Next*.

3. **Instala el panel.** Pestaña **Consoles** → **Bash**. En la pantalla negra que se abre, pega esto y pulsa Enter:

   ```
   git clone https://github.com/estebanguimi/harris-media-website.git && bash harris-media-website/desplegar/pythonanywhere.sh
   ```

   Tarda 1–2 minutos. Al final dice **«¡Listo!»** y te muestra tus links.

4. **Enciéndelo.** Vuelve a la pestaña **Web** y pulsa el botón verde **Reload**.

5. Abre `https://TU-USUARIO.pythonanywhere.com/admin` y **crea tu usuario y contraseña**.

## Para actualizarlo cuando cambie el código

En **Consoles → Bash**, pega lo siguiente y luego pulsa **Reload** en la pestaña Web:

```
bash harris-media-website/desplegar/pythonanywhere.sh
```

Tu contenido no se borra al actualizar.

## Límites de la cuenta gratis

- **512 MB de espacio.** Para los videos usa enlaces de YouTube, Vimeo, Facebook o Instagram en lugar de subir archivos MP4.
- **Cada 3 meses** PythonAnywhere te pide entrar y pulsar **«Run until 3 months from today»** en la pestaña Web. Si no lo haces, la web se pausa (no se borra nada).
- El link es `TU-USUARIO.pythonanywhere.com`. Para usar un dominio propio hace falta un plan de pago.
