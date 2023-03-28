# multi-stage build
FROM cgr.dev/chainguard/python:3.10-dev AS build

# install dependencies in a venv
RUN python -m venv /home/nonroot/venv
ENV PATH="/home/nonroot/venv/bin:$PATH"
WORKDIR /home/nonroot
COPY . /home/nonroot
RUN pip install -r requirements.txt

# run image
FROM cgr.dev/chainguard/python:3.10-dev

USER 65532
WORKDIR /home/nonroot
COPY --chown=nonroot:nonroot --from=build /home/nonroot /home/nonroot

# run container as nonroot user
ENV PATH="/home/nonroot/venv/bin:$PATH"
ENV PORT 8080
ENV GUNICORN_CMD_ARGS="--workers 2 --threads 4 -b 0.0.0.0:8080 --chdir /home/nonroot"
# Run the web service on container startup.
ENTRYPOINT [ "gunicorn", "app:app" ]