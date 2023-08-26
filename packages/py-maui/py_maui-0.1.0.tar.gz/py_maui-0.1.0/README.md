# Python MAUI

Python bindings for (rs-maui)[https://github.com/KrisNK/rs-maui].

## Installation

```
pip install py-maui
```

## Building the package

#### Setup
```
python -m venv .env
source .env/bin/activate
pip install maturin
```

#### Build in development
```
source .env/bin/activate
maturin develop
```

When coding within the environment, using `maturin develop` will build the package and it can be imported with `import py_maui`.

#### Publishing

For publishing, contact @KrisNK.


