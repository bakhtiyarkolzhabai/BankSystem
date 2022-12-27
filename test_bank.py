from decimal import Decimal

from bank import Bank
from client import Client
from transaction import TransactionState


def test_bank_create():
    bank = Bank.new_bank()
    assert isinstance(bank, Bank)
    assert isinstance(bank.clients, dict)


def test_check_transaction_normal_create():
    client1 = Client.from_names("Bill")
    client2 = Client.from_names("John")
    starting_amount = Decimal("100.500")

    bank = Bank.new_bank()
    bank.add_client(client1)
    bank.add_client(client2)
    transaction = bank.new_transaction(
        client_to=client2,
        amount=starting_amount,
    )

    assert transaction.state == TransactionState.CREATED
    assert bank.get_balance(client2.id) == Decimal("0")
    bank.complete_transaction(transaction=transaction)
    assert transaction.state == TransactionState.COMPLETED
    assert bank.get_balance(client2.id) == Decimal("100.500")

    transaction = bank.new_transaction(
        client_from=client2,
        client_to=client1,
        amount=Decimal("0.5")
    )

    assert bank.get_balance(client2.id) == Decimal("100.500")
    assert bank.get_balance(client1.id) == Decimal("0")
    bank.complete_transaction(transaction=transaction)
    assert bank.get_balance(client2.id) == Decimal("100")
    assert bank.get_balance(client1.id) == Decimal("0.5")
    assert transaction.state == TransactionState.COMPLETED


def test_transaction_error_state():
    client1 = Client.from_names("Bill")
    client2 = Client.from_names("John")
    starting_amount = Decimal("100.500")

    bank = Bank.new_bank()
    bank.add_client(client1)
    bank.add_client(client2)

    transaction = bank.new_transaction(
        client_to=client2,
        amount=starting_amount,
    )

    assert transaction.state == TransactionState.CREATED
    assert bank.get_balance(client2.id) == Decimal(0)
    bank.complete_transaction(transaction=transaction)
    assert transaction.state == TransactionState.COMPLETED
    assert bank.get_balance(client2.id) == Decimal("100.500")

    transaction = bank.new_transaction(
        client_from=client2,
        client_to=client1,
        amount=Decimal("200")
    )
    bank.complete_transaction(transaction=transaction)
    assert transaction.state == TransactionState.ERROR
    assert bank.get_balance(client2.id) == Decimal("100.500")
    assert bank.get_balance(client1.id) == Decimal("0")