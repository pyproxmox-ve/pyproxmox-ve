# pyproxmox-ve
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI Status](https://github.com/proxmox-central-manager/pyproxmox-ve/actions/workflows/ci.yml/badge.svg)](https://github.com/proxmox-central-manager/pyproxmox-ve/actions/workflows/ci.yml/badge.svg)

A simple python module to interact with the Proxmox Virtual Environment (PVE) HTTP API which uses aiohttp and pydantic.

## Installation

```
pip install pyproxmox-ve
```

## Pydantic
Pydantic is a fantastic data validation library which I've opted to use in this project, not only to provide data input validation (and also return validation from the PVE API responses), but also to provide a great developer experience with IDEs. Python type annotations provide us the ability with great integration with tools like PyCharm, VSCode and more...

## Examples

TO-DO

## Development and Contributing

See this document [which explains the development environment/setup required to contribute to this project](CONTRIBUTING.md)

