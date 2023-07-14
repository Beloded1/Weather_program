FROM python:3.11.0-alpine3.16

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app/

RUN python -m pip install -r requirements.txt

COPY app /app/app

ENTRYPOINT ["python", "-m", "app"]
