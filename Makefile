PYTHON = python3
MAIN = a_maze_ing.py
INPUT = config.txt
VENV = maze

.SILENT:

build:
	$(PYTHON) -m build

install:
	pip install -r requirements.txt 

setup: 
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -r requirements.txt

run:
	$(PYTHON) $(MAIN) $(INPUT)

debug:
	$(PYTHON) -m pdb $(MAIN) $(INPUT)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -type d -name dist -exec rm -rf {} +
	find . -type d -name mazegen.egg-info -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "output.txt" -delete

lint:
	$(PYTHON) -m flake8 . --exclude=maze
	mypy . --explicit-package-bases \
	        --warn-return-any \
	        --ignore-missing-imports \
	        --disallow-untyped-defs \
	        --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 . --exclude=maze
	mypy	--strict . \
	    	--explicit-package-bases
