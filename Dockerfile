FROM python:3.11.0-alpine3.16

WORKDIR /app

RUN python -m pip install --upgrade pip

COPY requirements.txt /app/

RUN python -m pip install -r requirements.txt

COPY weather_program /app/weather_program

CMD ["uvicorn", "weather_program.server:app", "--host", "0.0.0.0"]
