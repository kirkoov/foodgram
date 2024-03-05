FROM python:3.10

WORKDIR /app

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi"]
