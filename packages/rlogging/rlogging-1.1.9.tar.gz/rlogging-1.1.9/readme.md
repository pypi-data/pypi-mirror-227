# rLogging

Module with frequently used functions for advanced logging

[![PyPI](https://img.shields.io/pypi/v/rlogging)](https://pypi.org/project/rlogging/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/rlogging)](https://pypi.org/project/rlogging/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/rlogging)](https://gitlab.com/rocshers/python/rlogging)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/rlogging/branch/release/graph/badge.svg?token=RPFNZ8SBQ6)](https://codecov.io/gitlab/rocshers:python/rlogging)
[![Downloads](https://static.pepy.tech/badge/rlogging)](https://pepy.tech/project/rlogging)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/rlogging)](https://gitlab.com/rocshers/python/rlogging)

## Functionality

- Formatters
  - **JsonFormatter** - Convert log to json
  - **ElkFormatter** - Convert log to json for ELK parsing (one-dimensional array)
- Adapters
  - **HttpLoggerAdapter**
  - **HttpLoggerAdapter**
- Django
  - **DjangoLoggerAdapter**
  - **LoggingMiddleware**

## Usage

```
pip install rlogging
```

### Python

Normal logging setup with new classes

```bash

```

### Django

```bash
# settings.py

INSTALLED_APPS = [
    ...
    'rlogging.integration.django',
    ...
]

MIDDLEWARE = [
    ...
    'rlogging.integration.django.middleware.LoggingMiddleware',
    ...
]

LOGGING = ...
```

### FastAPI

```bash

```

### aiogram

```bash

```
