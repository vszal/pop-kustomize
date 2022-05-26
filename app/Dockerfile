# multi-stage build
FROM python:3.10-slim as build
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
build-essential gcc 
# install dependencies in a venv
WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# run image
FROM python:3.10-slim
RUN apt-get update
RUN apt-get install -y --no-install-recommends
# add nonroot group/user
RUN groupadd -g 999 nonroot && \
    useradd -r -u 999 -g nonroot nonroot
# mkdir the workdir with nonroot ownership
RUN mkdir /usr/app && chown nonroot:nonroot /usr/app
WORKDIR /usr/app
# copy in venv fromb build and app source files
COPY --chown=nonroot:nonroot --from=build /usr/app/venv ./venv
COPY --chown=nonroot:nonroot . .
# run container as nonroot user
USER 999
# add venv to the path
ENV PATH="/usr/app/venv/bin:$PATH"
ENV PORT 8080
ENV GUNICORN_CMD_ARGS="--workers 2 --threads 2 -b 0.0.0.0:8080 --chdir /usr/app"
# Run the web service on container startup.
CMD ["gunicorn",  "app:app"]