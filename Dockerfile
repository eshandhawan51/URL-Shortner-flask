FROM python:3.8-slim-buster

WORKDIR /url-shortner

RUN pip install redis
RUN pip install flask

COPY . .

CMD ["python3","shortner.py"]