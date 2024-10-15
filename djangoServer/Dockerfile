FROM python:3.10.14-alpine3.20

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN  apk update \
	&& apk add --no-cache gcc musl-dev postgresql-dev python3-dev libffi-dev build-base cmake ninja libjpeg-turbo-dev zlib-dev \
	&& pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install -r requirements.txt
COPY ./ ./



CMD ["python","manage.py","runserver","0.0.0.0:8000"]
