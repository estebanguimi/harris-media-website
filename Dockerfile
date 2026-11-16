# Para ponerlo en un servidor: docker build -t hmg-panel . && docker run -d -p 8000:8000 -v hmg-datos:/datos --restart unless-stopped hmg-panel
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV HOST=0.0.0.0 PORT=8000 HMG_DATA=/datos/contenido HMG_PUBLIC=/datos/sitio-publicado
VOLUME /datos
EXPOSE 8000
CMD ["python", "app.py"]
