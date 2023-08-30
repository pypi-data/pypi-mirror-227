# # Globals
# SHELL=/bin/bash
# PROJECT_NAME=populus-env
# PYTHON_INTERPRETER=python3
# CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh; conda deactivate; conda deactivate; conda activate
# ACTIVATE_PROJECT=$(CONDA_ACTIVATE) $(PROJECT_NAME)
# ARCHITECTURE=$(shell uname -m)

test:
	pytest

build:
	python3 -m build

dist: build
	python3 -m twine upload --verbose -u=__token__ dist/*

clean:
	rm dist/*