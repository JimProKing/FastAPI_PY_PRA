# Python 3.11 이미지 다운
FROM python:3.11-buster

# Python output unbuffered for Docker logs
ENV PYTHONUNBUFFERED=1

WORKDIR /src

# Install poetry
RUN pip install "poetry==1.6.1"

# Copy poetry file (do not require poetry.lock to allow resolving inside container)
COPY pyproject.toml ./

# Configure poetry to create .venv in-project and install dependencies if pyproject exists
RUN poetry config virtualenvs.in-project true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

# Run uvicorn via poetry (ensure api/main.py exists)
ENTRYPOINT ["poetry", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]