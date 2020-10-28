FROM python:3.9

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

RUN python -m 'scripts.build_assets'

EXPOSE 5000

CMD ["gunicorn", "--config=gunicorn.py", "wsgi:app"]
