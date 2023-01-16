# syntax=docker/dockerfile:1.4

FROM python:3.10-alpine AS builder
EXPOSE 8002
WORKDIR /matchStatus
COPY requirements.txt /matchStatus
RUN pip3 install -r requirements.txt
COPY . /matchStatus
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8002"]
