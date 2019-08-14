FROM python:3.6-alpine

MAINTAINER Stefan Kuznetsov (skuznetsov@posteo.net)

ADD . /mokujin

WORKDIR /mokujin

RUN pip install --user pipenv

RUN pipenv install --deploy --ignore-pipfile

CMD ["pipenv", "run", "python", "./mokujin.py"]