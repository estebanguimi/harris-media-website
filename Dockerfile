# To run it on a server: docker build -t hmg-web . && docker run -d -p 8000:8000 -v hmg-data:/data --restart unless-stopped hmg-web
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV HOST=0.0.0.0 PORT=8000 HMG_DATA=/data/content HMG_PUBLIC=/data/site
VOLUME /data
EXPOSE 8000
CMD ["python", "app.py"]
