# hello-pypi
Just seeing how to publish and version libraries for PyPI



``` bash
python -m venv myvenv
source myvenv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

``` bash
python setup.py sdist bdist_wheel
```

``` bash
twine upload dist/*
```

``` bash
python -m venv myvenv_test
source myvenv_test/bin/activate
python -m pip install --upgrade pip
pip install ./dist/mylibrary-0.1-py3-none-any.whl
```


