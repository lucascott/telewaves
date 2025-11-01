FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_FROZEN=true
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_NO_CACHE=true

WORKDIR /app
RUN mkdir -p /data /library && chmod 777 /data /library

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

COPY . .

RUN chmod -R 777 /app

CMD ["uv", "run", "--no-sync", "python", "-m", "telewaves"]
