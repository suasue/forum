FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/forum

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /