#!/usr/bin/python3

import pytest
import brownie
from brownie.test import given, strategy
from hypothesis import settings

@pytest.fixture
def token_foo(Token, accounts):
    return Token.deploy("Token Foo", "TKF", 18, 1e21, {'from': accounts[0]})

@pytest.fixture
def token_bar(Token, accounts):
    return Token.deploy("Token Bar", "TKB", 18, 1e21, {'from': accounts[0]})

@pytest.fixture
def exchange_house(ExchangeHouse, accounts):
    return ExchangeHouse.deploy(5, {'from': accounts[0]})

@pytest.fixture
def populate_accounts(token_foo, token_bar, exchange_house, accounts):
    token_foo.transfer(accounts[1], 1e10, {'from': accounts[0]})
    token_bar.transfer(accounts[1], 1e10, {'from': accounts[0]})
    token_foo.transfer(exchange_house, 1e10, {'from': accounts[0]})
    token_bar.transfer(exchange_house, 1e10, {'from': accounts[0]})

def test_swap_zero_tokens(token_foo, token_bar, exchange_house, populate_accounts, accounts):
    token_foo_balance = token_foo.balanceOf(accounts[1])
    token_bar_balance = token_bar.balanceOf(accounts[1])

    amount = 0

    token_foo.approve(exchange_house.address, amount, {'from': accounts[1]})
    exchange_house.swap(token_foo, token_bar, amount, {'from': accounts[1]})

    assert token_foo_balance == token_foo.balanceOf(accounts[1])
    assert token_bar_balance == token_bar.balanceOf(accounts[1])

@given(amount=strategy('uint256', max_value=1e5))
@settings(max_examples=5)
def test_swap_tokens(Token, ExchangeHouse, accounts, amount):
    token_foo = Token.deploy("Token A", "TKA", 18, 1e21, {'from': accounts[0]})
    token_bar = Token.deploy("Token B", "TKB", 18, 1e21, {'from': accounts[0]})

    exchange_house = ExchangeHouse.deploy(5, {'from': accounts[0]})

    token_foo.transfer(accounts[1], 1e10, {'from': accounts[0]})
    token_bar.transfer(accounts[1], 1e10, {'from': accounts[0]})
    token_foo.transfer(exchange_house, 1e10, {'from': accounts[0]})
    token_bar.transfer(exchange_house, 1e10, {'from': accounts[0]})

    token_foo_balance = token_foo.balanceOf(accounts[1])
    token_bar_balance = token_bar.balanceOf(accounts[1])

    token_foo.approve(exchange_house.address, amount, {'from': accounts[1]})
    exchange_house.swap(token_foo, token_bar, amount, {'from': accounts[1]})

    assert token_foo.balanceOf(accounts[1]) == token_foo_balance - amount
    assert token_bar.balanceOf(accounts[1]) == token_bar_balance + amount * 5

def test_swap_with_insufficient_balance_account (token_foo, token_bar, exchange_house, populate_accounts, accounts):
    amount = 1e11

    token_foo.approve(exchange_house.address, amount, {'from': accounts[1]})
    with brownie.reverts("Account insufficient balance"):
        exchange_house.swap(token_foo, token_bar, amount, {'from': accounts[1]})

def test_swap_with_insufficient_balance_exchange_house (Token, ExchangeHouse, accounts):
    token_foo = Token.deploy("Token A", "TKA", 18, 1e21, {'from': accounts[0]})
    token_bar = Token.deploy("Token B", "TKB", 18, 1e21, {'from': accounts[0]})

    exchange_house = ExchangeHouse.deploy(5, {'from': accounts[0]})

    token_foo.transfer(accounts[1], 1e10, {'from': accounts[0]})
    token_bar.transfer(accounts[1], 1e10, {'from': accounts[0]})
    token_foo.transfer(exchange_house, 1, {'from': accounts[0]})
    token_bar.transfer(exchange_house, 1, {'from': accounts[0]})
    
    amount = 1e5

    token_foo.approve(exchange_house.address, amount, {'from': accounts[1]})
    with brownie.reverts("Exchange House insufficient balance"):
        exchange_house.swap(token_foo, token_bar, amount, {'from': accounts[1]})

def test_swap_with_insufficient_allowance (token_foo, token_bar, exchange_house, populate_accounts, accounts):

    amount = 1e5

    token_foo.approve(exchange_house.address, amount-1, {'from': accounts[1]})
    with brownie.reverts("Insufficient allowance"):
        exchange_house.swap(token_foo, token_bar, amount, {'from': accounts[1]})

def test_swap_in_two_ways (token_foo, token_bar, exchange_house, populate_accounts, accounts):

    amount = 1e4

    token_foo_balance = token_foo.balanceOf(accounts[1])
    token_bar_balance = token_bar.balanceOf(accounts[1])

    token_foo.approve(exchange_house.address, amount, {'from': accounts[1]})
    exchange_house.swap(token_foo, token_bar, amount, {'from': accounts[1]})

    assert token_foo_balance - amount == token_foo.balanceOf(accounts[1]) 
    assert token_bar_balance + amount * 5 == token_bar.balanceOf(accounts[1])

    amount = 1e2

    token_foo_balance = token_foo.balanceOf(accounts[1])
    token_bar_balance = token_bar.balanceOf(accounts[1])

    token_bar.approve(exchange_house.address, amount, {'from': accounts[1]})
    exchange_house.swap(token_bar, token_foo, amount, {'from': accounts[1]})

    assert token_foo_balance + amount * 5== token_foo.balanceOf(accounts[1]) 
    assert token_bar_balance - amount == token_bar.balanceOf(accounts[1])

@given(rate=strategy('uint256', max_value=100))
@settings(max_examples=5)
def test_deployed_exchange_rate (ExchangeHouse, accounts, rate):
    exchange_house = ExchangeHouse.deploy(rate, {'from': accounts[0]})

    assert exchange_house.rate() == rate

@given(rate=strategy('uint256', min_value=1, max_value=100))
@settings(max_examples=5)
def test_set_exchange_rate (ExchangeHouse, accounts, rate):
    exchange_house = ExchangeHouse.deploy(rate, {'from': accounts[0]})

    exchange_house.set_rate(rate)

    assert exchange_house.rate() == rate

def test_set_exchange_rate_to_zero (ExchangeHouse, accounts):
    rate = 5

    exchange_house = ExchangeHouse.deploy(rate, {'from': accounts[0]})

    with brownie.reverts("Invalid rate"):
        exchange_house.set_rate(0)
