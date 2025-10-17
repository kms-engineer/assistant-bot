# How build package

## Requirements

setup.py
pyproject.toml

## Commands
Project contains build scripts: ```build_package.sh``` or ```build_package.bat```

### Linux / MacOS
Before running the script, make sure it has execute permissions. You can set the permissions using the command `chmod +x build_package.sh` on Unix-based systems.)
```shell
  chmod +x ./scripts/build_package.sh
```

You can run it from root folder of the project:
```shell
  ./scripts/build_package.sh
```

### Windows
On Windows you can run ```build_package.bat``` from root folder of the project:
```shell
  .\scripts\build_package.bat
```

### Manual (from console)
Alternatively, you can build the package using Python's build module with the following commands:
```shell
python -m pip install --upgrade pip setuptools wheel build
python -m build
```

### Build artefacts
After running the build command, the distribution files will be created in the `dist/` directory of your project.