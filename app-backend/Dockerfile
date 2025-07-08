FROM python:3.13-slim

ENV DEBUG=False
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get upgrade \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app
RUN --mount=from=ghcr.io/astral-sh/uv:latest,source=/uv,target=/bin/uv \
    uv sync -nq --no-dev

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

EXPOSE 8000
CMD ["bash", "/app/entrypoint.sh"]