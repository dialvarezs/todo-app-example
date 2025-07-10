#!/usr/bin/env bash
set -e

alembic upgrade head

litestar \
    run \
    --host 0.0.0.0 \
    --port 8000 \
    --web-concurrency 4
