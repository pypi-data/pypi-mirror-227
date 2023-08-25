# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['responsaas', 'responsaas.routes']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.101.1,<0.102.0', 'pydantic>=2.2.0,<3.0.0', 'responses>=0.17.0']

extras_require = \
{'pmr': ['pytest-mock-resources[docker]>=2.8.0']}

setup_kwargs = {
    'name': 'responsaas',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Responsaas\n\n[![Actions Status](https://github.com/dancardin/responsaas/workflows/test/badge.svg)](https://github.com/dancardin/responsaas/actions)\n[![Coverage Status](https://coveralls.io/repos/github/DanCardin/responsaas/badge.svg?branch=main)](https://coveralls.io/github/DanCardin/responsaas?branch=main)\n[![Documentation Status](https://readthedocs.org/projects/responsaas/badge/?version=latest)](https://responsaas.readthedocs.io/en/latest/?badge=latest)\n[![Docker](https://img.shields.io/docker/cloud/build/dancardin/responsaas?label=Docker&style=flat)](https://hub.docker.com/r/dancardin/responsaas)\n\nWraps the python [responses](https://github.com/getsentry/responses) library As\nA Service.\n\nSee the full documentation [here](https://responsaas.readthedocs.io/en/latest/)\n(or more specifically\n[converting from responses](https://responsaas.readthedocs.io/en/latest/converting)).\n\n## Quickstart\n\n### Automatic (with pytest)\n\nUsing\n[pytest-mock-resources](https://github.com/schireson/pytest-mock-resources/), we\ncan use Docker to manage the lifecycle of the server.\n\n`pip install responsaas[pmr]`\n\n```python\nfrom responsaas.pytest import create_responsaas_fixture, create_responsaas_server_fixture\n\nresponsaas_server = create_responsaas_server_fixture()\nresponsaas = create_responsaas_fixture()\n\ndef test_foo(responsaas: Responsaas):\n    responsaas.add("/foo", json={"bar": True})\n\n    response = requests.get(responsaas.base_url + "/foo")\n    assert response.json() == {"bar": True}\n```\n\n### Manual\n\nThe manual examples assume you have some external way of standing up the server\n\n`pip install responsaas`\n\n```python\nimport requests\nfrom responsaas import ResponsaasServer, Responsaas\n\n# With pytest\nfrom responsaas.pytest import create_responsaas_fixture\n\nresponsaas = create_responsaas_fixture("http://localhost:7564")\n\ndef test_foo(responsaas: Responsaas):\n    responsaas.add("/foo", json={"bar": True})\n\n    response = requests.get(responsaas.base_url + "/foo")\n    assert response.json() == {"bar": True}\n\n\n# Or completely manually.\ndef test_foo():\n    responsaas_server = ResponsaasServer("http://localhost:7564")\n    with responsaas_server.activate() as responsaas:\n        responsaas.add("/foo", json={"bar": True})\n\n        response = requests.get(responsaas.base_url + "/foo")\n        assert response.json() == {"bar": True}\n```\n\n## Why?!?\n\nUnder the hood, `repsonses` is `patch`ing the network calls being made and\nreplacing their result with the result you specify. It\'s very fast, convenient,\nand (by default) disallows you from making **actual** network calls.\n\n**However** the same (`patch`) strategy that makes it useful has some issues.\n\n- This can run afoul of other libraries which perform `patch` operations. The\n  issue history of responses has many instances (frequently with `moto`), where\n  patches get clobbered in one way or another.\n\n  - `responsaas` does not use `patch` at all. It is a real standalone service\n    responding to real requests.\n\n- Either through `patch` issues, or through programmer error, `responses` can be\n  **so** non-invasive that API calls accidentally get made through to the\n  original destination URL.\n\n  - `responsaas` forces you to change (or really, make configurable) the URL\n    you\'re hitting for tests, which should make it impossible to hit the\n    original destination url in tests on accident.\n\n- `responses` allows you to return arbitrary python objects (like exceptions)\n  which wouldn\'t be possible for a request to actually return.\n\n  - `responsaas` (once again), is a literal service responding to requests. The\n    requesting client code is receiving bytes over the wire, and parsing it\n    normally.\n\n- `responses` is(?) limited to mocking the `requests` library. Which doesn\'t\n  cover cases like `httpx`, `aiohttp`, etc.\n\n  - `responsaas` is client agnostic, given that it\'s a real service.\n\n- `responses` needs an additional mechanism to allow "passthru" requests\n\n  - `responsaas` (once again), is a literal service responding to requests, so\n    it can only return.\n\n## How?\n\nWhat\'s going on internally is:\n\n- Each test registers a new "namespace" against the `responsaas` server\n- Each new namespace corresponds to one `responses.RequestsMock`.\n- As incoming requests are received by the server, they\'re mapped to the request\n  shape expected by `responses`, and routed directly through its request\n  matching and responds logic.\n',
    'author': 'DanCardin',
    'author_email': 'ddcardin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
