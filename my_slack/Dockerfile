FROM python:3.14-slim-bullseye

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "app.py"]
