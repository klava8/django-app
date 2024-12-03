FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install django -i https://repo.huaweicloud.com/repository/pypi/simple/

COPY . .

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]