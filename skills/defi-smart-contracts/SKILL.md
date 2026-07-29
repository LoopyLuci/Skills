---
name: defi-smart-contracts
description: "Use when building DeFi smart contracts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [DeFi, smart-contracts, AMM, lending, staking, yield, Solidity]
    related_skills: [blockchain-development-solidity, tokenomics-design, zero-knowledge-proofs, agent-economics-markets]
---

# DeFi Smart Contracts

Building DeFi smart contracts — from AMMs and lending protocols through staking, yield optimization, and security patterns for DeFi.

## When to Use

- Building decentralized exchange (DEX) contracts
- Implementing lending/borrowing protocols
- Staking and yield farming contracts
- DeFi security (flash loan attacks, oracle manipulation)

## DeFi Patterns

```solidity
// Simple AMM (constant product)
contract ConstantProductAMM {
    uint public reserve0;
    uint public reserve1;
    
    function swap(uint amountIn, address tokenIn) external returns (uint) {
        (uint r0, uint r1) = tokenIn == token0 ? (reserve0, reserve1) : (reserve1, reserve0);
        uint amountOut = (amountIn * r1) / (r0 + amountIn);  // x*y=k invariant
        _transfer(tokenOut, amountOut);
        (reserve0, reserve1) = tokenIn == token0 ? 
            (r0 + amountIn, r1 - amountOut) : (r0 - amountOut, r1 + amountIn);
        return amountOut;
    }
    
    // Flash loan pattern
    function flashLoan(uint amount, address token) external {
        uint balanceBefore = IERC20(token).balanceOf(address(this));
        IERC20(token).transfer(msg.sender, amount);
        IFlashBorrower(msg.sender).execute();  // arbitrary callback
        require(IERC20(token).balanceOf(address(this)) >= balanceBefore, "Not repaid");
    }
}
```

## Verification Checklist

- [ ] Contract audited by third-party firm
- [ ] Oracle manipulation resistance (TWAP or multiple oracles)
- [ ] Flash loan attack vectors mitigated
- [ ] Reentrancy guard on all state-changing functions
- [ ] Access control (admin, pause, emergency functions)
- [ ] Economic parameters validated (fees, slippage, reserves)
- [ ] Testnet deployment verified before mainnet
