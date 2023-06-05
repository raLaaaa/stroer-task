FROM python:3.9

ENV PYTHONFAULTHANDLER=1 \
PYTHONUNBUFFERED=1 \
PYTHONHASHSEED=random \
PIP_NO_CACHE_DIR=off \
PIP_DISABLE_PIP_VERSION_CHECK=on \
PIP_DEFAULT_TIMEOUT=100 \
POETRY_VERSION=1.3.2

# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
&& poetry install $(test "$BUILD_TYPE" = production && echo "--no-dev") --no-interaction --no-ansi

# Creating folders, and files for a project:
COPY stroer_coding_challenge /app/stroer_coding_challenge/
# RUN poetry run python /app/stroer_coding_challenge/manage.py migrate

EXPOSE 8000

# CMD ["python", "stroer_coding_challenge/manage.py", "runserver", "0.0.0.0:8000"]
