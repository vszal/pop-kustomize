FROM debian:11-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /opt/venv/bin/pip install --disable-pip-version-check -r /requirements.txt

# Copy the virtualenv into a distroless image (use :debug-nonroot for tools)
FROM gcr.io/distroless/python3:nonroot
COPY --from=build-venv /opt/venv /opt/venv
COPY --chown=nonroot:nonroot . /home/nonroot
# gunicorn needs this path
ENV PYTHONPATH=/opt/venv/lib/python3.9/site-packages
WORKDIR /opt/venv/bin
# Service must listen to $PORT environment variable.
ENV PORT 8080
ENV GUNICORN_CMD_ARGS="--workers 2 --threads 2 -b 0.0.0.0:8080 --chdir /home/nonroot"
# Run the web service on container startup.
CMD ["gunicorn",  "app:app"]