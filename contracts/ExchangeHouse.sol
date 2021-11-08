pragma solidity ^0.8.0;

// SPDX-License-Identifier: MIT

/**
    @title A ERC-20 token exchange house implementation
 */

contract ExchangeHouse {

    constructor() {}

    /**
        @notice Return token_b to msg.sender based on the received amount of
                token_a and the exchange rate
     */
    function swap(
        address _token_a,
        address _token_b,
        uint256 _value
    ) 
        public 
        returns (bool) 
    {
        return true;
    }

}
