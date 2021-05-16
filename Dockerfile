FROM python:3.7

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/forum

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
