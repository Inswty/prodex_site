FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

ENV FLASK_ENV=production

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "tngt_app.wsgi"]
