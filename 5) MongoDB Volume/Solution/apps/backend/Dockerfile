FROM python:3.8-slim AS base

FROM base AS python_dependencies
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .

FROM python_dependencies AS production
RUN pipenv install --system --deploy --ignore-pipfile

WORKDIR /app
COPY . /app

USER root
ENV FLASK_ENV production
CMD flask run --host=0.0.0.0 -p 8080