.PHONY: install
install:
	pip install -e .
	pip install -e ."[devel]"

.PHONY: format
format:
	find src -name "*.py" | xargs black
	black setup.py
