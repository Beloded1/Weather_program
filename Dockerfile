FROM python:3.10.8-slim
WORKDIR /app

# install requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

ENV PORT=8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]