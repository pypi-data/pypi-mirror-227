"""
Main interface for managedblockchain-query service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_managedblockchain_query import (
        Client,
        ListTokenBalancesPaginator,
        ListTransactionEventsPaginator,
        ListTransactionsPaginator,
        ManagedBlockchainQueryClient,
    )

    session = Session()
    client: ManagedBlockchainQueryClient = session.client("managedblockchain-query")

    list_token_balances_paginator: ListTokenBalancesPaginator = client.get_paginator("list_token_balances")
    list_transaction_events_paginator: ListTransactionEventsPaginator = client.get_paginator("list_transaction_events")
    list_transactions_paginator: ListTransactionsPaginator = client.get_paginator("list_transactions")
    ```
"""
from .client import ManagedBlockchainQueryClient
from .paginator import (
    ListTokenBalancesPaginator,
    ListTransactionEventsPaginator,
    ListTransactionsPaginator,
)

Client = ManagedBlockchainQueryClient


__all__ = (
    "Client",
    "ListTokenBalancesPaginator",
    "ListTransactionEventsPaginator",
    "ListTransactionsPaginator",
    "ManagedBlockchainQueryClient",
)
