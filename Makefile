.PHONY: test lint typecheck run pre-commit

test:
	pytest -v

lint:
	ruff check .

typecheck:
	mypy .

run:
	uv run main.py 

pre-commit: lint typecheck test
