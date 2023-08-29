# hello-pypi
Just seeing how to publish and version libraries for PyPI


## Development
``` bash
python -m venv myvenv
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Build Wheel
``` bash
bash build.sh
```

## Integration Test (local wheel build)
``` bash
bash build.sh
```

## Publish to PyPI
Make sure to bump version in setup.py
``` bash
twine upload dist/*
```

## Prod test PyPI
``` bash
twine upload dist/*
```

``` bash
python -m venv myvenv_test
source myvenv_test/bin/activate
python -m pip install --upgrade pip
pip install ./dist/markslibrary-0.1-py3-none-any.whl
```

``` bash
python -m venv myvenv_prod
source myvenv_prod/bin/activate
python -m pip install --upgrade pip
pip install markslibrary
```
