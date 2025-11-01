export UV_FROZEN=true

format:
	uv run ruff format
	uv run ruff check --fix-only

lint:
	uv run ruff check
	uv run mypy .
