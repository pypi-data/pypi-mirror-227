[![Datalayer](https://assets.datalayer.tech/datalayer-25.svg)](https://datalayer.io)

[![Become a Sponsor](https://img.shields.io/static/v1?label=Become%20a%20Sponsor&message=%E2%9D%A4&logo=GitHub&style=flat&color=1ABC9C)](https://github.com/sponsors/datalayer)

# 🪐 🐳 Jupyter Docker

> Manage Docker from Jupyter.

For MacOS

- https://github.com/docker/docker-py/issues/3059
- https://github.com/gh640/wait-for-docker/issues/12
- Allow the default Docker socket to be used (requires password)

```bash
pip install -e .[test]
jupyter labextension develop . --overwrite
jupyter labextension list
jupyter server extension list
yarn jupyterlab
```
