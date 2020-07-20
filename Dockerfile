FROM python:3.8-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev libffi-dev

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

# This may need tweaking
CMD ["gunicorn", "--config=gunicorn.py", "wsgi:app"]