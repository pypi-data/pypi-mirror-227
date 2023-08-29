1. Setup venv
2. Install `twine` & `build`
3. `python -m build`
3. `twine check dist/*`
4. `twine upload -r pypi dist/*`