---
name: blockchain-development-solidity
description: "Use when developing blockchain and Solidity smart contracts."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [blockchain, Solidity, smart-contracts, Ethereum, EVM, Web3, DeFi]
    related_skills: [defi-smart-contracts, zero-knowledge-proofs, tokenomics-design, web3-integration]
---

# Blockchain and Solidity Development

Developing smart contracts on Ethereum-compatible blockchains — from Solidity fundamentals and contract patterns through security, gas optimization, and deployment.

## When to Use

- Writing and deploying Ethereum smart contracts
- Building DeFi, NFT, or token applications
- Auditing contract security
- Optimizing gas costs

## Solidity Patterns

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract TokenVault {
    mapping(address => uint256) public balances;
    event Deposited(address indexed user, uint256 amount);
    
    // Reentrancy guard pattern
    bool private _locked;
    modifier noReentrant() {
        require(!_locked, "Reentrancy");
        _locked = true;
        _;
        _locked = false;
    }
    
    function deposit() external payable {
        balances[msg.sender] += msg.value;
        emit Deposited(msg.sender, msg.value);
    }
    
    function withdraw(uint256 amount) external noReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```

## Verification Checklist

- [ ] Contract follows checks-effects-interactions pattern
- [ ] Reentrancy guard on external calls
- [ ] Access control (Ownable, RBAC) implemented
- [ ] Integer overflow protection (Solidity 0.8+ has built-in)
- [ ] Gas optimization (pack structs, use events, avoid loops)
- [ ] Contract verified on Etherscan/block explorer
- [ ] Audit by third-party firm (for production contracts)
- [ ] Test coverage (Hardhat/Foundry) for all functions
