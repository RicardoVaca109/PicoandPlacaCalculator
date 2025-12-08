# Dockerfile para un proyecto Flask. Ajusta `app:app` al módulo/objeto correcto (ej. wsgi:app, main:app)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Dependencias del sistema (añade/remueve según necesites)
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar dependencias primero para aprovechar cache de docker
COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Ejecutar como usuario no-root
RUN useradd -m appuser || true
USER appuser

EXPOSE 5000

# Comando por defecto: usa gunicorn. Reemplaza "app:app" por tu módulo Flask si es necesario.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app"]