PYTHON = python3
MAIN = a_maze_ing.py
INPUT = input.txt
VENV = maze

.SILENT:

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
	find . -name "*.pyc" -delete

lint:
	$(PYTHON) -m flake8 .
	mypy . --explicit-package-bases \
	        --warn-return-any \
	        --ignore-missing-imports \
	        --disallow-untyped-defs \
	        --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	mypy	--strict . \
	    	--explicit-package-bases
