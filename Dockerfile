FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	build-essential \
	libpq-dev \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["python", "tierra_media_web/manage.py", "runserver", "0.0.0.0:8000"]

