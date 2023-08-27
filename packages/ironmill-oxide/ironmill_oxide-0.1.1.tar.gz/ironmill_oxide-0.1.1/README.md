# pdm - Project Dependency Manager

Starting to develop the CL tool written in python.

I propose that our package-manager have the following traits:
1. Version specifier is version (Not Branch or revision)
2. No lock-file present (Shallow dependency trees)
3. Not synced (Expected large file sizes)
4. PDM (Project dependency manager)
5. "Asymmetric" - Bundles we grab and projects we are used in are different: Circuit manifests and project manifests look different

Install with one of these commands based on your python3 / pip versions:
```
python3 -m pip install --editable .
pip install --editable .
pip3 install --editable .
```

Then once it is installed you can call:
```
oxide init
> Create new circuits.toml manifest
oxide add foo
> Added circuit foo
oxide rm bar
> Circuit bar not listed in the dependencies
oxide add bar
> Added circuit bar
oxide rm foo
> Removed circuit foo
```

# pdm unit testing

To run the full test of suites, first ensure you have pytest installed:
```
poetry install
```
Then run the following command from the root of this project:
```
poetry run pytest
```
You should see something like:
```
============ X passed, Y failed, Z warning in 2.12s ==============
```
