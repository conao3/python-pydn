# pydn

A lightweight tool for running single-file Python scripts with automatic dependency management.

## Overview

pydn lets you declare dependencies directly in your Python scripts using special comments. When you run a script with pydn, it automatically creates an isolated virtual environment, installs the required packages, and executes your code. Dependencies are cached for fast subsequent runs.

## Installation

```bash
pip install pydn
```

Or install from source:

```bash
git clone https://github.com/conao3/python-pydn.git
cd python-pydn
pip install .
```

## Usage

Add dependency declarations to your Python script using `# pydn:` comments:

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

Then run your script with pydn:

```bash
pydn your_script.py
```

On the first run, pydn will:
1. Create a virtual environment specific to your script
2. Install the declared dependencies
3. Execute your script

Subsequent runs use the cached environment for instant execution.

## Syntax

Dependencies are declared with comments at the top of your file:

```python
# pydn: package~=version
```

You can specify multiple dependencies:

```python
# pydn: requests~=2.31.0
# pydn: pandas~=2.0.0
# pydn: matplotlib~=3.8.0
```

The version specifier follows standard pip syntax (`~=`, `>=`, `==`, etc.).

## How It Works

- Virtual environments are stored in `~/.cache/pydn/venv/`
- Each script gets its own isolated environment (identified by file path hash)
- Dependency installations are cached and only re-run when declarations change

## Requirements

- Python 3.11 or later

## License

Apache-2.0
