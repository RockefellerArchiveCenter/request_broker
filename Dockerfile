FROM python:3.10

ENV PYTHONUNBUFFERED 1
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --upgrade "pip>=26.2.2" && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ADD . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
