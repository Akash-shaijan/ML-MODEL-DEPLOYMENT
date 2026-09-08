FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# --host 0.0.0.0 is required here (not 127.0.0.1): inside a container,
# 127.0.0.1 only accepts connections from within the container itself.
# Requests coming from outside (e.g. your browser hitting localhost:8000
# on the host machine) arrive through the container's external network
# interface, which 0.0.0.0 listens on but 127.0.0.1 does not.

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
