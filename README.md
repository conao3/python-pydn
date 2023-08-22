# python-pydn

Onefile python script with resolving dependency.

## Usage

```bash
poetry install
poetry run pydn sample/02_pyyaml/pyyaml.py
```

## Syntax

Add `# pydn: <package>~=<version>` to the top of the file.
`pydn` will create venv and install the package, then run the script.

```python
# pydn: pyyaml~=6.0.1

import yaml

raw = '''\
name: John Smith
age: 33
'''

data = yaml.safe_load(raw)
print(data)
```
