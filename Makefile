.PHONY: test lint typecheck run pre-commit

test:
	pytest -v

lint:
	ruff check .

typecheck:
	mypy .

run:
	uv run python -m myapp

pre-commit: lint typecheck test
