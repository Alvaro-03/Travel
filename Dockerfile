FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY . .

# Puerto por defecto para el servidor web
ENV PORT=8080
EXPOSE 8080

# Iniciar servidor web y monitor en segundo plano
CMD ["python", "web_server.py"]
