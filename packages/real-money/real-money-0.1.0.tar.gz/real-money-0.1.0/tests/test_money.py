"""Money tests"""

from decimal import Decimal

import pytest

from money.currency import Currency
from money.exceptions import (
    CurrencyMismatchError,
    InvalidAmountError,
    InvalidOperandError,
)
from money.money import Money

# pylint: disable=unneeded-not,expression-not-assigned,no-self-use,missing-docstring
# pylint: disable=misplaced-comparison-constant,singleton-comparison,too-many-public-methods


class TestMoney:
    """Money tests"""

    def test_construction(self):
        money = Money("3.95", Currency.USD)
        assert money.amount == Decimal("3.95")
        assert money.currency == Currency.USD

        money = Money("1", Currency.USD)
        assert money.amount == Decimal("1")
        assert money.currency == Currency.USD

        money = Money("199", Currency.JPY)
        assert money.amount == Decimal("199")
        assert money.currency == Currency.JPY

        money = Money("192.325", Currency.KWD)
        assert money.amount == Decimal("192.325")
        assert money.currency == Currency.KWD

        with pytest.raises(InvalidAmountError):
            Money("3.956", Currency.USD)

        with pytest.raises(InvalidAmountError):
            # nonfractional currency
            Money("10.2", Currency.KRW)

    def test_from_sub_units(self):
        money = Money.from_sub_units(101, Currency.USD)
        assert money == Money("1.01", Currency.USD)

        money = Money.from_sub_units(5, Currency.JPY)
        assert money == Money("5", Currency.JPY)

    def test_sub_units(self):
        money = Money("1.01", Currency.USD)
        assert money.sub_units == 101

    def test_hash(self):
        assert hash(Money("1.2", Currency.USD)) == hash(Money("1.2", Currency.USD))
        assert hash(Money("1.5", Currency.EUR)) != hash(Money("9.3", Currency.EUR))
        assert hash(Money("99.3", Currency.CHF)) != hash(Money("99.3", Currency.USD))

    def test_tostring(self):
        assert str(Money("1.2", Currency.USD)) == "USD 1.2"
        assert str(Money("3.6", Currency.CHF)) == "CHF 3.6"
        assert str(Money("88", Currency.JPY)) == "JPY 88"

    def test_less_than(self):
        assert Money("1.2", Currency.USD) < Money("3.5", Currency.USD)
        assert not Money("104.2", Currency.EUR) < Money("5.13", Currency.EUR)
        assert not Money("2.2", Currency.GBP) < Money("2.2", Currency.GBP)

        with pytest.raises(CurrencyMismatchError):
            Money("1.2", Currency.GBP) < Money("3.5", Currency.EUR)

        with pytest.raises(InvalidOperandError):
            1.2 < Money("3.5", Currency.USD)

    def test_less_than_or_equal(self):
        assert Money("1.2", Currency.USD) <= Money("3.5", Currency.USD)
        assert not Money("104.2", Currency.EUR) <= Money("5.13", Currency.EUR)
        assert Money("2.2", Currency.GBP) <= Money("2.2", Currency.GBP)

        with pytest.raises(CurrencyMismatchError):
            Money("1.2", Currency.GBP) <= Money("3.5", Currency.EUR)

        with pytest.raises(InvalidOperandError):
            1.2 <= Money("3.5", Currency.USD)

    def test_greater_than(self):
        assert Money("3.5", Currency.USD) > Money("1.2", Currency.USD)
        assert not Money("5.13", Currency.EUR) > Money("104.2", Currency.EUR)
        assert not Money("2.2", Currency.GBP) > Money("2.2", Currency.GBP)

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) > Money("1.2", Currency.GBP)

        with pytest.raises(InvalidOperandError):
            Money("3.5", Currency.USD) > 1.2

    def test_greater_than_or_equal(self):
        assert Money("3.5", Currency.USD) >= Money("1.2", Currency.USD)
        assert not Money("5.13", Currency.EUR) >= Money("104.2", Currency.EUR)
        assert Money("2.2", Currency.GBP) >= Money("2.2", Currency.GBP)

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) >= Money("1.2", Currency.GBP)

        with pytest.raises(InvalidOperandError):
            Money("3.5", Currency.USD) >= 1.2

    def test_equal(self):
        assert Money("3.5", Currency.USD) == Money("3.5", Currency.USD)
        assert Money("4.0", Currency.GBP) == Money("4.0", Currency.GBP)
        assert not Money("6.9", Currency.USD) == Money("43", Currency.USD)

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) == Money("3.5", Currency.GBP)

        with pytest.raises(InvalidOperandError):
            Money("5.5", Currency.USD) == 5.5

    def test_not_equal(self):
        assert Money("3.5", Currency.USD) != Money("46.44", Currency.USD)
        assert Money("4.0", Currency.GBP) != Money("12.01", Currency.GBP)
        assert not Money("6.9", Currency.USD) != Money("6.9", Currency.USD)

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) != Money("23", Currency.GBP)

        with pytest.raises(InvalidOperandError):
            Money("5.5", Currency.USD) != 666.32

    def test_bool(self):
        assert bool(Money("3.62", Currency.USD)) == True
        assert bool(Money("0.00", Currency.USD)) == False

    def test_add(self):
        assert Money("3.5", Currency.USD) + Money("1.25", Currency.USD) == Money(
            "4.75", Currency.USD
        )

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) + Money("23", Currency.GBP)

        with pytest.raises(InvalidOperandError):
            Money("5.5", Currency.USD) + 666.32

        with pytest.raises(InvalidOperandError):
            666.32 + Money("5.5", Currency.USD)

    def test_subtract(self):
        assert Money("3.5", Currency.USD) - Money("1.25", Currency.USD) == Money(
            "2.25", Currency.USD
        )
        assert Money("4", Currency.EUR) - Money("5.5", Currency.EUR) == Money(
            "-1.5", Currency.EUR
        )

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) - Money("1.8", Currency.GBP)

        with pytest.raises(InvalidOperandError):
            Money("5.5", Currency.USD) - 6.32

        with pytest.raises(InvalidOperandError):
            666.32 - Money("5.5", Currency.USD)

    def test_multiply(self):
        assert Money("3.2", Currency.USD) * 3 == Money("9.6", Currency.USD)
        assert 3 * Money("3.2", Currency.EUR) == Money("9.6", Currency.EUR)
        assert Money("9.95", Currency.USD) * 0.15 == Money("1.49", Currency.USD)
        assert Money("3", Currency.JPY) * 0.2 == Money("1", Currency.JPY)
        assert Money("3", Currency.KRW) * 1.5 == Money("5", Currency.KRW)

        assert Money("3", Currency.JPY) * 1.4995 == Money("4", Currency.JPY)
        assert Money("3", Currency.GNF) * 1.4995 == Money("4", Currency.GNF)

        with pytest.raises(InvalidOperandError):
            Money("5.5", Currency.USD) * Money("1.2", Currency.USD)

    def test_divide(self):
        assert Money("3.3", Currency.USD) / 3 == Money("1.1", Currency.USD)
        assert Money("9.95", Currency.EUR) / 0.24 == Money("41.46", Currency.EUR)
        assert Money("3", Currency.JPY) / 1.6 == Money("2", Currency.JPY)
        assert Money("3.6", Currency.GBP) / Money("2.5", Currency.GBP) == 1.44

        with pytest.raises(TypeError):
            3 / Money("5.5", Currency.USD)

        with pytest.raises(ZeroDivisionError):
            Money("3", Currency.USD) / 0

        with pytest.raises(ZeroDivisionError):
            Money("3.3", Currency.USD) / 0.0

        with pytest.raises(ZeroDivisionError):
            Money("3.3", Currency.USD) / Money("0", Currency.USD)

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) / Money("1.8", Currency.GBP)

    def test_floor_divide(self):
        assert Money("3.3", Currency.USD) // 3 == Money("1", Currency.USD)
        assert Money("9.95", Currency.EUR) // 0.24 == Money("41", Currency.EUR)
        assert Money("3", Currency.JPY) // 1.6 == Money("1", Currency.JPY)
        assert Money("3.6", Currency.GBP) // Money("2.5", Currency.GBP) == 1

        with pytest.raises(TypeError):
            3 // Money("5.5", Currency.USD)

        with pytest.raises(ZeroDivisionError):
            Money("3", Currency.USD) // 0

        with pytest.raises(ZeroDivisionError):
            Money("3.3", Currency.USD) // 0.0

        with pytest.raises(ZeroDivisionError):
            Money("3.3", Currency.USD) // Money("0", Currency.USD)

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) // Money("1.8", Currency.GBP)

    def test_mod(self):
        assert Money("3.3", Currency.USD) % 3 == Money("0.3", Currency.USD)
        assert Money("3", Currency.JPY) % 2 == Money("1", Currency.JPY)
        assert Money("3", Currency.EUR) % Money("2", Currency.EUR) == 1

        with pytest.raises(TypeError):
            3 % Money("5.5", Currency.USD)

        with pytest.raises(ZeroDivisionError):
            Money("3.3", Currency.USD) % 0

        with pytest.raises(ZeroDivisionError):
            Money("3.3", Currency.USD) % 0.0

        with pytest.raises(CurrencyMismatchError):
            Money("3.5", Currency.EUR) % Money("1.8", Currency.GBP)

    def test_neg(self):
        assert -Money("5.23", Currency.USD) == Money("-5.23", Currency.USD)
        assert -Money("-1.35", Currency.EUR) == Money("1.35", Currency.EUR)

    def test_pos(self):
        assert +Money("5.23", Currency.USD) == Money("5.23", Currency.USD)
        assert +Money("-1.35", Currency.EUR) == Money("-1.35", Currency.EUR)

    def test_abs(self):
        assert abs(Money("5.23", Currency.USD)) == Money("5.23", Currency.USD)
        assert abs(Money("-1.35", Currency.EUR)) == Money("1.35", Currency.EUR)

    def test_format(self):
        assert Money("3.24", Currency.USD).format("en_US") == "$3.24"
        assert Money("5.56", Currency.EUR).format("es_ES") == "5,56\xa0€"
        assert Money("7.31", Currency.GBP).format("en_UK") == "£7.31"
        assert Money("10", Currency.JPY).format("en_US") == "¥10"
        assert Money("94", Currency.JPY).format("ja_JP") == "￥94"
