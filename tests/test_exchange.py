#!/usr/bin/python3

import pytest

@pytest.fixture
def token_foo(Token, accounts):
    return Token.deploy("Token Foo", "TKF", 18, 1e21, {'from': accounts[0]})

@pytest.fixture
def token_bar(Token, accounts):
    return Token.deploy("Token Bar", "TKB", 18, 1e21, {'from': accounts[0]})

@pytest.fixture
def exchange_house(ExchangeHouse, accounts):
    return ExchangeHouse.deploy({'from': accounts[0]})

def test_swap_zero_tokens (token_foo, token_bar, exchange_house, accounts):
    token_foo_balance_before = token_foo.balanceOf(accounts[0])
    token_bar_balance_before = token_bar.balanceOf(accounts[0])

    amount = 0

    exchange_house.swap(token_foo.address, token_bar.address, amount, {'from': accounts[0]})

    assert token_foo_balance_before == token_foo.balanceOf(accounts[0])
    assert token_bar_balance_before == token_bar.balanceOf(accounts[0])
