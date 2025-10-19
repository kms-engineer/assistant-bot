# Installation and setup

Below are concise, structured instructions to prepare the project and install the package.

Replace `<package-name>` and `<version>` examples with the actual name/version.

## 1) Prerequisites
- Install Python (specify supported major/minor, e.g., 3.10+).  
- Ensure pip is up-to-date: `python -m pip install --upgrade pip`.
- (Optional) Install platform build deps if the package has native extensions:
    - Debian/Ubuntu: `sudo apt-get install build-essential python3-dev libssl-dev`
    - macOS (Homebrew): `brew install openssl`
    - Windows: install Visual Studio Build Tools / appropriate SDKs
- (Optional) Install `python -m pip install build` if you will build wheels locally.

## 2) Use a virtual environment (recommended)

- Create and activate:
  - Unix/macOS: `python -m venv .venv && source .venv/bin/activate`
  - Windows (Powershell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
- Confirm active: `which python` / `python -V`.

## 3) Install from PyPI (public release)

- Basic: `pip install <package-name>`
- Specific version: `pip install <package-name>==<version>`
- Version ranges: `pip install '<package-name>=1.0.*,>=1.0.0'`
- Extras: `pip install '<package-name>[extra1,extra2]'`
- Upgrade: `pip install --upgrade <package-name>`
- Pre-release: `pip install --pre <package-name>`

## 4) Install using requirements files

- requirements.txt format supports pinned packages:
  - Example line: `<package-name>==1.2.3`
- Install: `pip install -r requirements.txt`
- Use separate files for dev/test: `requirements-dev.txt`
- Manage pins with pip-tools: `pip-compile` / `pip-sync`.

## 5) Install from a local .whl (wheel)

- Install a wheel file: `pip install ./dist/<package-name>-1.2.3-py3-none-any.whl`
- Install from a local directory of wheels without contacting PyPI:
  - `pip install --no-index --find-links=dist <package-name>`
- Build a wheel from source:
  - `python -m build` (outputs to `dist/`)
  - legacy: `python setup.py bdist_wheel`

## 6) Install from local source directory or editable install

- From local directory (non-editable): `pip install /path/to/project`
- Editable (install for development): `pip install -e /path/to/project`
- From a Git repo:
  - Non-editable: `pip install git+https://github.com/user/repo.git@v1.2.3#egg=<package-name>`
  - Editable: `pip install -e git+https://github.com/user/repo.git@main#egg=<package-name>`


## 7) Dependency management tools (alternatives)

- Poetry: `poetry add <package-name>` or define in `pyproject.toml`, then `poetry install`
- Pipenv: `pipenv install <package-name>`

## 8) System / runtime preparation before running

- Set required environment variables (documented in project README or `.env`).
- Populate config files or secrets (use `.env` or secret manager).
- Run tests: `pytest` or project-specific test command.

## 9) Quick checklist to run locally

- [ ] Create & activate virtualenv
- [ ] Install package and dependencies (`pip install -r requirements.txt` or `pip install <package-name>`)
- [ ] Set environment variables / .env
- [ ] Install system packages for native deps if needed
- [ ] Run DB migrations and any build steps
- [ ] Start application: `python -m <app>` or project-specific start command

Replace placeholders and platform specifics with actual project details where necessary.