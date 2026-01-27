# ============================================================================
# PHASE 3: OOP & Classes - PROBLEMS
# ============================================================================
# Practice problems for Phase 3 concepts.
# Run tests: npm run test:py -- python/phase3/problems.py

# -----------------------------------------------------------------------------
# PROBLEM 1: BankAccount
# -----------------------------------------------------------------------------
# Create a BankAccount class with:
# - __init__ that takes owner (str) and optional starting balance (default 0)
# - deposit(amount) method - adds to balance, returns new balance
# - withdraw(amount) method - subtracts from balance if sufficient funds
#   - if insufficient funds, raise ValueError with message "Insufficient funds"
#   - returns new balance on success
# - balance property (read-only) - returns current balance
# - __repr__ that returns "BankAccount(owner='...', balance=...)"
#
# Hints:
# - Use @property for read-only balance
# - Store balance in self._balance (underscore = private convention)
# - Remember to validate withdrawal amount
#
# JS equivalent:
# class BankAccount {
#   constructor(owner, balance = 0) {
#     this.owner = owner;
#     this._balance = balance;
#   }
#   get balance() { return this._balance; }
#   deposit(amount) { this._balance += amount; return this._balance; }
#   withdraw(amount) {
#     if (amount > this._balance) throw new Error("Insufficient funds");
#     this._balance -= amount;
#     return this._balance;
#   }
# }


class BankAccount:
    pass  # YOUR CODE HERE


def test_bank_account():
    # Basic creation
    acc = BankAccount("Alice")
    assert acc.owner == "Alice"
    assert acc.balance == 0

    # With starting balance
    acc2 = BankAccount("Bob", 100)
    assert acc2.balance == 100

    # Deposit
    result = acc2.deposit(50)
    assert result == 150
    assert acc2.balance == 150

    # Withdraw success
    result = acc2.withdraw(30)
    assert result == 120
    assert acc2.balance == 120

    # Withdraw insufficient funds
    try:
        acc2.withdraw(200)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Insufficient funds" in str(e)

    # Balance unchanged after failed withdrawal
    assert acc2.balance == 120

    # __repr__
    assert repr(acc2) == "BankAccount(owner='Bob', balance=120)"
