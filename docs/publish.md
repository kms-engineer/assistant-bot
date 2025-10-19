# Publish a Python wheel (.whl) to PyPI

Short checklist and commands to build and publish a wheel to TestPyPI and PyPI.

## Prerequisites
- Project with a valid pyproject.toml or setup.cfg/setup.py and an updated version.
- Python and pip installed.
- Clean build artifacts: remove `dist/`, `build/`, `*.egg-info` before building.

## Install tooling
```bash
pip install --upgrade build twine
```
Links: Packaging guide (building) — https://packaging.python.org/en/latest/ (see "Creating distribution archives")  
Twine — https://pypi.org/project/twine/

## Build the wheel
```bash
# creates dist/*.whl and dist/*.tar.gz
python -m build
# or only wheel
python -m build --wheel
```
Verify `dist/` contains `your_package‑X.Y.Z‑py3-none-any.whl`.

## Create a PyPI API token
- Create account on PyPI: https://pypi.org/
- Create an API token in your account settings: https://pypi.org/manage/account/
- Note: use username `__token__` and the token string as password with twine. See API token docs: https://packaging.python.org/en/latest/guides/using-pypi/#using-api-tokens

Optionally save credentials in `~/.pypirc` or export env vars:
```bash
export TWINE_USERNAME="__token__"
export TWINE_PASSWORD="pypi-...your-token..."
```
Guide for .pypirc — https://packaging.python.org/en/latest/guides/using-pypirc/

## Test upload to TestPyPI (recommended)
```bash
# upload to TestPyPI
twine upload --repository testpypi dist/*
# install from TestPyPI to verify
pip install --index-url https://test.pypi.org/simple/ --no-deps your-package==X.Y.Z
```
TestPyPI — https://test.pypi.org/  
Using TestPyPI guide — https://packaging.python.org/en/latest/guides/using-testpypi/

## Upload to production PyPI
```bash
twine upload dist/*
```
After upload verify:
```bash
pip install your-package==X.Y.Z
```

## Common issues / tips
- Increment package version for each release (PyPI rejects duplicate version).
- Remove old files in `dist/` before building to avoid uploading old artifacts.
- If upload fails with authentication, confirm token value and that username is `__token__`.
- Check wheel compatibility tags (platform-specific wheels vs pure Python).
- For more packaging details and best practices, read the Packaging User Guide: https://packaging.python.org/en/latest/

Quick reference: PyPI home — https://pypi.org/
