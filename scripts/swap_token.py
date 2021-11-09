#!/usr/bin/python3

import time
from brownie import *

def main():

    rate = 5

    token_foo = Token.deploy("Token Foo", "TKF", 18, 1e21, {'from': accounts[0]})
    token_bar = Token.deploy("Token Bar", "TKB", 18, 1e21, {'from': accounts[0]})
    exchange_house = ExchangeHouse.deploy(
        rate,
        {'from': accounts[0]}
    )

    # Distribute tokens among the accounts
    token_foo.transfer(accounts[1], 100, {'from': accounts[0]})
    token_bar.transfer(accounts[1], 100, {'from': accounts[0]})

    # Distribute tokens among the exchange house smartcontracts
    token_foo.transfer(exchange_house.address, 1e10, {'from': accounts[0]})
    token_bar.transfer(exchange_house.address, 1e10, {'from': accounts[0]})

    foo_amount = 10

    # Approve to Exchange House to take the tokens Foo
    token_bar.approve(exchange_house.address, foo_amount, {'from': accounts[1]})

    # Perform the swap of the tokens
    balance = exchange_house.swap(
        token_bar,
        token_foo,
        foo_amount,
        {'from': accounts[1]}
    )

    exchange_house.set_rate(9)

    # Approve to Exchange House to take the tokens Foo
    token_bar.approve(exchange_house.address, foo_amount, {'from': accounts[1]})

    # Perform the swap of the tokens
    balance = exchange_house.swap(
        token_bar,
        token_foo,
        foo_amount,
        {'from': accounts[1]}
    )
