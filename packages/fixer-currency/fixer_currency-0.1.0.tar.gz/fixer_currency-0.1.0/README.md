# Fixer Currency

A Python module for the Fixer API for currency conversion.

[![PyPI - Version](https://img.shields.io/pypi/v/fixer-currency.svg)](https://pypi.org/project/fixer-currency)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fixer-currency.svg)](https://pypi.org/project/fixer-currency)
![Github Build Status](https://github.com/jfrid/fixer-currency/actions/workflows/build-and-inspect-main.yml/badge.svg)

-----

**Table of Contents**

- [Module Description](#module-description)
- [Installation](#installation)
- [License](#license)
- [Account and API Key](#account-and-api-key)
- [Usage](#usage)

## Module Description

Fixer API (formerly known as Fixer.io) is a JSON API for current and
historical foreign exchange rates published by the European Central Bank.

The rates are updated daily around 13:00 CET.

This module is based on the module [fixerio](https://pypi.org/project/fixerio/)
originally created by by Adrián Matellanes.

## Installation

```console
pip install fixer-currency
```

## License

`fixer-currency` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Account and API Key

All calls to the Fixer API requires an API key. To acquire an API key you need
to first register for an account on [API Layer]. When logged in, go to the
[Fixer API page] and subscribe to one of the plans. The free plan allows for
quite a number of requests per month and has no other restrictions as to what
can be requested through the API.

## Usage

All requests to the Fixer API should be made using an instance of the `FixerClient` class.

```python
from fixer_currency import FixerClient

fxr = FixerClient("<YOUR API KEY>")
```

The `FixerClient` object always has a base currency defined for conversions and
the default currency is EUR. Another base currency can be specified with an
argument:

```python
fxr = FixerClient("<YOUR API KEY>", "USD")
```

List all available currencys that can be used as base or target in a conversion:

```python
>>> fxr.available_currencies()
{'success': True, 'symbols': {'AED': 'United Arab Emirates Dirham', 'AFN': 'Afghan Afghani', 'ALL': 'Albanian Lek', ... }}
```

Get latest rate(s) for one or more currencies:

```python
>>> fxr.latest(symbols=["SEK", "NOK"])
{'success': True, 'timestamp': 1692526623, 'base': 'EUR', 'date': '2023-08-20', 'rates': {'SEK': 11.938802, 'NOK': 11.611995}}
```

Get historical rates for any day since 1999:

```python
>>> import datetime
>>> fxr.historical_rates(datetime.date(2022, 1,1), symbols="SEK")
{'success': True, 'timestamp': 1641081599, 'historical': True, 'base': 'EUR', 'date': '2022-01-01', 'rates': {'SEK': 10.291223}}
```

[API Layer]: https://apilayer.com/
[Fixer API page]: https://apilayer.com/marketplace/fixer-api
