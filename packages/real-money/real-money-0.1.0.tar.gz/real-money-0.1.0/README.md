# real-money

[![Latest PyPI version](https://badge.fury.io/py/real-money.svg)](https://badge.fury.io/py/real-money)

Money class for Python 3.7 and higher. Forked from [py-money][]. It has been
forked as the original library seems unmantained, and some of the currencies
have changed since the last update.

Unlike other Python money classes, this class enforces that all monetary
amounts are represented with the correct number of decimal places for the
currency. For example, 3.678 USD is invalid, as is 5.5 JPY.

## Installation

Install the latest release with:

```sh
pip install real-money
```

If you want to have localised formatting, you should install with
[`Babel`][babel]:

```sh
pip install real-money[babel]
```

## Usage

A `Money` object can be created with an amount (specified as a string) and a
currency from the `Currency` class:

```python
from money import Currency, Money
m = Money("9.95", Currency.GBP)
m
# GBP 9.95
```

If you try to use more decimals than declared for the currency in the
[ISO 4217][] standard, it will throw an error:

```python
m = Money("4.624", Currency.EUR)
# InvalidAmountError: Invalid amount for currency
m = Money("1200.5", Currency.JPY)
# InvalidAmountError: Invalid amount for currency
```

`Money` objects can also be created from and converted to sub units:

```python
m = Money.from_sub_units(499, Currency.USD)
m
# USD 4.99
m.sub_units
# 499
```

`Money` is inmutable and supports most mathematical and logical operators:

```python
m = Money("10.00", Currency.USD)
m / 2
# USD 5.00
m + Money("3.00", Currency.USD)
# USD 13.00
m > Money("5.55", Currency.USD)
# True
m < Money("5.55", Currency.USD)
# False
```

`Money` will automatically round to the correct number of decimal places for
the currency:

```python
m = Money("9.95", Currency.EUR)
m * 0.15
# EUR 1.49
m = Money("10", Currency.JPY)
m / 3
# JPY 3
```

Money can be formatted for different locales (if you have `Babel`):

```python
Money("3.24", Currency.USD).format("en_US")
# $3.24
Money("9.95", Currency.EUR).format("es_ES")
# 9,95 €
Money("7.36", Currency.EUR).format("en_UK")
# £7.36
Money("94", Currency.JPY).format("ja_JP")
# ￥94
```

`Money` does not support conversion between currencies. Mathematical and
logical operations between two money objects are only allowed if both objects
are of the same currency. Otherwise, an error will be thrown:

```python
Money("1.25", Currency.USD) + Money("2", Currency.EUR)
# CurrencyMismatchError: Currencies must match
```

For more examples, check out the test file!

## Acknowledgements
`real-money` is a fork of [py-money][].

Much of the code is borrowed from [carlospalol/money][]. Much of the logic for
handling foreign currencies is taken from [sebastianbergmann/money][]. Money
formatting is powered by [Babel][babel].

[py-money]: https://github.com/vimeo/py-money
[babel]: https://babel.pocoo.org/en/latest/
[ISO 4217]: https://en.wikipedia.org/wiki/ISO_4217
[carlospalol/money]: https://github.com/carlospalol/money
[sebastianbergmann/money]: https://github.com/sebastianbergmann/money
