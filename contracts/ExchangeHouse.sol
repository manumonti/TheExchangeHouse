pragma solidity ^0.6.0;

// SPDX-License-Identifier: MIT

import "./Token.sol";

/**
    @title A ERC-20 token exchange house implementation
    @notice This smartcontract swap between two ERC-2- tokens applying a
            exchange rate that can be updated.
 */

contract ExchangeHouse {

    uint128 public rate;
    address public rate_admin;

    constructor(
        uint128 _rate
    ) 
    public 
    {
        rate = _rate;
        rate_admin = msg.sender;
    }

    /**
        @notice Return an amount of tokens_b to msg.sender based on the 
                received amount of token_a and the current exchange rate
        @param _token_source_add The address of the deployed token to send
        @param _token_target_add The address of the deployed token to receive
        @param _amount The amount of tokens to send
        @return The amount of tokens received
     */
    function swap(
        address _token_source_add,
        address _token_target_add,
        uint256 _amount
    )
        public returns (uint256)
    {
        uint256 token_target_amount = _amount * rate;

        Token token_source = Token(_token_source_add);
        Token token_target = Token(_token_target_add);

        require(token_source.balanceOf(msg.sender) >= _amount, "Account insufficient balance");
        require(token_target.balanceOf(address(this)) >= token_target_amount, "Exchange House insufficient balance");
        require(token_source.allowance(msg.sender, address(this)) >= _amount, "Insufficient allowance");

        token_source.transferFrom(msg.sender, address(this), _amount);
        token_target.transfer(msg.sender, token_target_amount);

        return token_target_amount;
    }
    
    /**
    @notice Set the exchange rate. Only available for the account that 
            deployed the contract (admin rate)
    @param _rate The exchange rate to set
    @return True if the action was succesfully performed
     */

    function set_rate(uint128 _rate) public returns (bool) {
        require(rate_admin == msg.sender );
        require(_rate > 0, "Invalid rate");

        rate = _rate;

        return true;
    }
}
