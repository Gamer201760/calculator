.PHONY: test lint typecheck run pre-commit

help:
	@echo "Доступные команды:"
	@echo "  make install      - Установить все зависимости"
	@echo "  make infix        - Запустить калькулятор в инфиксном режиме"
	@echo "  make rpn          - Запустить калькулятор в режиме RPN"
	@echo "  make test         - Запустить тесты pytest"
	@echo "  make lint         - Запустить линтер ruff"
	@echo "  make typecheck    - Запустить проверку типов mypy"
	@echo "  make pre-commit   - Запустить все проверки (lint, typecheck, test)"

install:
	uv sync

test:
	uv run pytest -v

lint:
	uv run ruff check .

typecheck:
	uv run mypy .

infix:
	uv run main.py 

rpn:
	uv run main.py --rpn

pre-commit: lint typecheck test
