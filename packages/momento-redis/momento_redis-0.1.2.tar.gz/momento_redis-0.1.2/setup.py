# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['momento_redis', 'momento_redis.utils']

package_data = \
{'': ['*']}

install_requires = \
['momento==1.7.1', 'redis==4.6.0', 'typing-extensions==4.5.0']

setup_kwargs = {
    'name': 'momento-redis',
    'version': '0.1.2',
    'description': 'Momento wrapper for redis/redis-py',
    'long_description': '<img src="https://docs.momentohq.com/img/logo.svg" alt="logo" width="400"/>\n\n[![project status](https://momentohq.github.io/standards-and-practices/badges/project-status-official.svg)](https://github.com/momentohq/standards-and-practices/blob/main/docs/momento-on-github.md)\n[![project stability](https://momentohq.github.io/standards-and-practices/badges/project-stability-alpha.svg)](https://github.com/momentohq/standards-and-practices/blob/main/docs/momento-on-github.md) \n\n\n# Momento Python Redis compatibility client\n\n## What and why?\n\nThis project provides a Momento-backed implementation of [redis/redis-py](https://github.com/redis/redis-py)\nThe goal is to provide a drop-in replacement for [redis/redis-py](https://github.com/redis/redis-py) so that you can\nuse the same code with either a Redis server or with the Momento Cache service!\n\n## Usage\n\nTo switch your existing `redis/redis-py` application to use Momento, you only need to change the code where you construct\nyour client object:\n\n### With redis-py client\n\n```python\n# Import the redis module\nfrom redis import Redis\n# Replace these values with your Redis server\'s details\n_REDIS_HOST = \'my.redis-server.com\';\n_REDIS_PORT = 6379;\n_REDIS_DB = 0\n_REDIS_PASSWORD = \'mypasswd\';\n# Create a Redis client\nredis_client = Redis(host=_REDIS_HOST, port=_REDIS_PORT, db=_REDIS_DB, password=_REDIS_PASSWORD)\n```\n\n### With Momento\'s Redis compatibility client\n\n```python\nimport datetime\n# Import the Momento redis compatibility client.\nimport momento\nfrom momento_redis import MomentoRedis\n\n_CACHE_NAME = "my-cache"\n# Initialize Momento client.\nredis_client = MomentoRedis(\n    momento.CacheClient(\n        momento.Configurations.Laptop.latest(),\n        momento.CredentialProvider.from_environment_variable("MOMENTO_AUTH_TOKEN"),\n        datetime.timedelta(seconds=60)\n    ),\n    _CACHE_NAME\n)\n```\n\n**NOTE**: The Momento `redis/redis-py` implementation currently supports simple key/value pairs (`GET`, `SET`, `DELETE`) \nas well as `INCR/INCRBY` and `DECR/DECRBY`. We will continue to add support for additional Redis APIs in the future; \nfor more information see the [current Redis API support](#current-redis-api-support) section later in this doc.\n\n## Installation\n\nThe Momento Python Redis compatibility client is [available on PyPi](https://pypi.org/project/momento-redis/).\nYou can install it via:\n\n```bash\npoetry add momento-redis\n```\n\n## Examples\n\n### Prerequisites\n\nTo run these examples, you will need a Momento auth token. You can generate one using the [Momento Console](https://console.gomomento.com).\n\nThe examples will utilize the auth token via an environment variable `MOMENTO_AUTH_TOKEN` that you set.\n\n### Basic example\n\nIn the [`examples/`](./examples/) directory, you will find a simple CLI app, `basic.py`, that does some basic sets and \ngets on strings. It uses the Momento Redis client by default, but you can also pass a \'-r\' flag on the command line \nto use a Redis client instead to verify that the two clients are functioning identically. You may also pass a \n\'-h <hostname>\' flag and/or a \'-p <port>\' flag to specify a specific host and port for the Redis client. By \ndefault, `localhost` and `6379` are used.\n\nHere\'s an example run against Momento Cache:\n\n```bash\ncd examples/\nexport MOMENTO_AUTH_TOKEN=<your momento auth token goes here>\npython basic.py\n```\n\nAnd the output should look like this:\n\n```bash\nIssuing a \'get\' for \'key1\', which we have not yet set.\nresult: None\nIssuing a \'set\' for \'key1\', with value \'value1\'.\nresult: True\nIssuing another \'get\' for \'key1\'.\nresult: b\'bar\'\ndone\n```\n\nRunning the script using Redis (`python basic.py -r`) should produce identical output.\n\n## Current Redis API Support\n\nThis library supports the most popular Redis APIs, but does not yet support all Redis APIs. We currently support the most\ncommon APIs related to string values (GET, SET, DELETE, INCR, DECR). We will be adding support for additional\nAPIs in the future. If there is a particular API that you need support for, please drop by our [Discord](https://discord.com/invite/3HkAKjUZGq)\nor e-mail us at [support@momentohq.com](mailto:support@momentohq.com) and let us know!\n\n### Type Checking\n\nTo allow the use of tools such as `mypy` and in-IDE type checking to tell you if you\'re using any APIs that we \ndon\'t support yet, we provide our own `MomentoRedisBase` abstract base class which explicitly lists out \nthe APIs we currently support. Simply use the class as a type annotation for your client:\n\n```python\nfrom momento_redis import MomentoRedis, MomentoRedisBase\nredis_client: MomentoRedisBase = MomentoRedis(...)\n```\n\nOnce the client is typed using the abstract base class, static analysis tools will allow you to find \ncalls to as yet unsupported APIs.\n\n----------------------------------------------------------------------------------------\nFor more info, visit our website at [https://gomomento.com](https://gomomento.com)!\n',
    'author': 'Momento',
    'author_email': 'hello@momentohq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
