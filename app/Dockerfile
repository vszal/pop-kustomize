# Distroless Dockerfile for running in production
FROM python:alpine3.7 AS build-env

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM gcr.io/distroless/python3
COPY --from=build-env /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY --from=build-env /usr/local/bin/gunicorn /home/worker/gunicorn
ENV PATH="/home/worker:${PATH}"
COPY . /home/worker

WORKDIR /home/worker
ENV PYTHONPATH=/usr/local/lib/python3.7/site-packages
# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 8080
ENV GUNICORN_CMD_ARGS="--workers 2 --threads 2 -b 0.0.0.0:8080 --chdir /home/worker"
# Run the web service on container startup.
CMD ["gunicorn",  "app:app"]