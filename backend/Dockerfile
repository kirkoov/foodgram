FROM python:3.10

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app

COPY . .

CMD ["python", "manage.py", "runserver", "0:9080"]

