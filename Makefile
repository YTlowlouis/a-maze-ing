PYTHON = python3
PIP = pip

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py config.txt

build:
	python3 -m build

lint:
	flake8 mazegen/*.py
	flake8 a_maze_ing.py
	flake8 config_loader.py
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs



clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -path "*/.mypy_cache/3.10" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

