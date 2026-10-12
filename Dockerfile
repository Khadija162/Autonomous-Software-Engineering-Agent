FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agent ./agent
COPY backend ./backend
COPY frontend ./frontend
COPY sample_repo ./sample_repo
EXPOSE 8000
CMD ["uvicorn","backend.main:app","--host","0.0.0.0","--port","8000"]
