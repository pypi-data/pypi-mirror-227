setup:
	pip3 install black twine build pdoc3
docs:
	pdoc3 --html -o docs src/simpleusers/users.py
format: setup
	black .
build: format
	python3 -m build
check: build
	twine check dist/*
upload: check docs
	twine upload -r pypi dist/*