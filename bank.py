from dataclasses import dataclass
from decimal import Decimal
from typing import Optional
from uuid import UUID

from client import Client
from transaction import TransactionState, Transaction


@dataclass
class Bank:
    clients: dict[UUID, Client]
    transactions: list[Transaction]

    @classmethod
    def new_bank(cls) -> "Bank":
        return cls(
            clients=dict(),
            transactions=list(),
        )

    def get_balance(self, client_id: UUID) -> Decimal:
        assert client_id in self.clients
        client = self.clients[client_id]
        result = Decimal(0)
        for transaction in self.transactions:
            if transaction.state == TransactionState.COMPLETED:
                if client == transaction.client_to:
                    result += transaction.amount
                if client == transaction.client_from:
                    result -= transaction.amount
        return result

    def new_transaction(self,
                        client_to: Client,
                        amount: Decimal,
                        client_from: Optional[Client] = None, ) -> Transaction:

        transaction = Transaction.new_transaction(client_from=client_from,
                                                  client_to=client_to,
                                                  amount=amount,
                                                  )
        self.transactions.append(transaction)
        return transaction

    def add_client(self, client: Client):
        if client.id not in self.clients:
            self.clients[client.id] = client

    def complete_transaction(self,
                             transaction: Transaction, ):

        if transaction.state != TransactionState.CREATED:
            return

        if transaction.client_from is not None:
            if self.get_balance(client_id=transaction.client_from.id) < transaction.amount:
                transaction.state = TransactionState.ERROR
                return

        transaction.state = TransactionState.COMPLETED
        return
