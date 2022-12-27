from decimal import Decimal

from transaction import Transaction
from client import Client


def test_transaction_create():
    client1 = Client.from_names("John")
    client2 = Client.from_names("Bill")

    transaction = Transaction.new_transaction(
        client_from=client1,
        client_to=client2,
        amount=Decimal(100),
    )

    assert isinstance(transaction, Transaction)
    assert transaction.client_from.name == "John"
    assert transaction.client_to.name == "Bill"
