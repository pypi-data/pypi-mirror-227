"""
Type annotations for managedblockchain-query service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_managedblockchain_query/type_defs/)

Usage::

    ```python
    from mypy_boto3_managedblockchain_query.type_defs import OwnerIdentifierTypeDef

    data: OwnerIdentifierTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence, Union

from .literals import (
    ErrorTypeType,
    QueryNetworkType,
    QueryTransactionEventTypeType,
    QueryTransactionStatusType,
    SortOrderType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "OwnerIdentifierTypeDef",
    "TokenIdentifierTypeDef",
    "ResponseMetadataTypeDef",
    "BlockchainInstantPaginatorTypeDef",
    "TimestampTypeDef",
    "GetTransactionInputRequestTypeDef",
    "TransactionTypeDef",
    "OwnerFilterTypeDef",
    "PaginatorConfigTypeDef",
    "TokenFilterTypeDef",
    "ListTransactionEventsInputRequestTypeDef",
    "TransactionEventTypeDef",
    "ListTransactionsSortTypeDef",
    "TransactionOutputItemTypeDef",
    "TokenBalancePaginatorTypeDef",
    "BlockchainInstantTypeDef",
    "GetTransactionOutputTypeDef",
    "ListTransactionEventsInputListTransactionEventsPaginateTypeDef",
    "ListTokenBalancesInputListTokenBalancesPaginateTypeDef",
    "ListTokenBalancesInputRequestTypeDef",
    "ListTransactionEventsOutputTypeDef",
    "ListTransactionsInputListTransactionsPaginateTypeDef",
    "ListTransactionsOutputTypeDef",
    "ListTokenBalancesOutputPaginatorTypeDef",
    "BatchGetTokenBalanceErrorItemTypeDef",
    "BatchGetTokenBalanceInputItemTypeDef",
    "BatchGetTokenBalanceOutputItemTypeDef",
    "GetTokenBalanceInputRequestTypeDef",
    "GetTokenBalanceOutputTypeDef",
    "ListTransactionsInputRequestTypeDef",
    "TokenBalanceTypeDef",
    "BatchGetTokenBalanceInputRequestTypeDef",
    "BatchGetTokenBalanceOutputTypeDef",
    "ListTokenBalancesOutputTypeDef",
)

OwnerIdentifierTypeDef = TypedDict(
    "OwnerIdentifierTypeDef",
    {
        "address": str,
    },
)

TokenIdentifierTypeDef = TypedDict(
    "TokenIdentifierTypeDef",
    {
        "network": QueryNetworkType,
        "contractAddress": NotRequired[str],
        "tokenId": NotRequired[str],
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

BlockchainInstantPaginatorTypeDef = TypedDict(
    "BlockchainInstantPaginatorTypeDef",
    {
        "time": NotRequired[datetime],
    },
)

TimestampTypeDef = Union[datetime, str]
GetTransactionInputRequestTypeDef = TypedDict(
    "GetTransactionInputRequestTypeDef",
    {
        "transactionHash": str,
        "network": QueryNetworkType,
    },
)

TransactionTypeDef = TypedDict(
    "TransactionTypeDef",
    {
        "network": QueryNetworkType,
        "transactionHash": str,
        "transactionTimestamp": datetime,
        "transactionIndex": int,
        "numberOfTransactions": int,
        "status": QueryTransactionStatusType,
        "to": str,
        "blockHash": NotRequired[str],
        "blockNumber": NotRequired[str],
        "from": NotRequired[str],
        "contractAddress": NotRequired[str],
        "gasUsed": NotRequired[str],
        "cumulativeGasUsed": NotRequired[str],
        "effectiveGasPrice": NotRequired[str],
        "signatureV": NotRequired[int],
        "signatureR": NotRequired[str],
        "signatureS": NotRequired[str],
        "transactionFee": NotRequired[str],
        "transactionId": NotRequired[str],
    },
)

OwnerFilterTypeDef = TypedDict(
    "OwnerFilterTypeDef",
    {
        "address": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

TokenFilterTypeDef = TypedDict(
    "TokenFilterTypeDef",
    {
        "network": QueryNetworkType,
        "contractAddress": NotRequired[str],
        "tokenId": NotRequired[str],
    },
)

ListTransactionEventsInputRequestTypeDef = TypedDict(
    "ListTransactionEventsInputRequestTypeDef",
    {
        "transactionHash": str,
        "network": QueryNetworkType,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

TransactionEventTypeDef = TypedDict(
    "TransactionEventTypeDef",
    {
        "network": QueryNetworkType,
        "transactionHash": str,
        "eventType": QueryTransactionEventTypeType,
        "from": NotRequired[str],
        "to": NotRequired[str],
        "value": NotRequired[str],
        "contractAddress": NotRequired[str],
        "tokenId": NotRequired[str],
        "transactionId": NotRequired[str],
        "voutIndex": NotRequired[int],
    },
)

ListTransactionsSortTypeDef = TypedDict(
    "ListTransactionsSortTypeDef",
    {
        "sortBy": NotRequired[Literal["TRANSACTION_TIMESTAMP"]],
        "sortOrder": NotRequired[SortOrderType],
    },
)

TransactionOutputItemTypeDef = TypedDict(
    "TransactionOutputItemTypeDef",
    {
        "transactionHash": str,
        "network": QueryNetworkType,
        "transactionTimestamp": datetime,
    },
)

TokenBalancePaginatorTypeDef = TypedDict(
    "TokenBalancePaginatorTypeDef",
    {
        "balance": str,
        "atBlockchainInstant": BlockchainInstantPaginatorTypeDef,
        "ownerIdentifier": NotRequired[OwnerIdentifierTypeDef],
        "tokenIdentifier": NotRequired[TokenIdentifierTypeDef],
        "lastUpdatedTime": NotRequired[BlockchainInstantPaginatorTypeDef],
    },
)

BlockchainInstantTypeDef = TypedDict(
    "BlockchainInstantTypeDef",
    {
        "time": NotRequired[TimestampTypeDef],
    },
)

GetTransactionOutputTypeDef = TypedDict(
    "GetTransactionOutputTypeDef",
    {
        "transaction": TransactionTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTransactionEventsInputListTransactionEventsPaginateTypeDef = TypedDict(
    "ListTransactionEventsInputListTransactionEventsPaginateTypeDef",
    {
        "transactionHash": str,
        "network": QueryNetworkType,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTokenBalancesInputListTokenBalancesPaginateTypeDef = TypedDict(
    "ListTokenBalancesInputListTokenBalancesPaginateTypeDef",
    {
        "tokenFilter": TokenFilterTypeDef,
        "ownerFilter": NotRequired[OwnerFilterTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTokenBalancesInputRequestTypeDef = TypedDict(
    "ListTokenBalancesInputRequestTypeDef",
    {
        "tokenFilter": TokenFilterTypeDef,
        "ownerFilter": NotRequired[OwnerFilterTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

ListTransactionEventsOutputTypeDef = TypedDict(
    "ListTransactionEventsOutputTypeDef",
    {
        "events": List[TransactionEventTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTransactionsInputListTransactionsPaginateTypeDef = TypedDict(
    "ListTransactionsInputListTransactionsPaginateTypeDef",
    {
        "address": str,
        "network": QueryNetworkType,
        "fromBlockchainInstant": NotRequired[BlockchainInstantPaginatorTypeDef],
        "toBlockchainInstant": NotRequired[BlockchainInstantPaginatorTypeDef],
        "sort": NotRequired[ListTransactionsSortTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTransactionsOutputTypeDef = TypedDict(
    "ListTransactionsOutputTypeDef",
    {
        "transactions": List[TransactionOutputItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTokenBalancesOutputPaginatorTypeDef = TypedDict(
    "ListTokenBalancesOutputPaginatorTypeDef",
    {
        "tokenBalances": List[TokenBalancePaginatorTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

BatchGetTokenBalanceErrorItemTypeDef = TypedDict(
    "BatchGetTokenBalanceErrorItemTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
        "errorType": ErrorTypeType,
        "tokenIdentifier": NotRequired[TokenIdentifierTypeDef],
        "ownerIdentifier": NotRequired[OwnerIdentifierTypeDef],
        "atBlockchainInstant": NotRequired[BlockchainInstantTypeDef],
    },
)

BatchGetTokenBalanceInputItemTypeDef = TypedDict(
    "BatchGetTokenBalanceInputItemTypeDef",
    {
        "tokenIdentifier": TokenIdentifierTypeDef,
        "ownerIdentifier": OwnerIdentifierTypeDef,
        "atBlockchainInstant": NotRequired[BlockchainInstantTypeDef],
    },
)

BatchGetTokenBalanceOutputItemTypeDef = TypedDict(
    "BatchGetTokenBalanceOutputItemTypeDef",
    {
        "balance": str,
        "atBlockchainInstant": BlockchainInstantTypeDef,
        "ownerIdentifier": NotRequired[OwnerIdentifierTypeDef],
        "tokenIdentifier": NotRequired[TokenIdentifierTypeDef],
        "lastUpdatedTime": NotRequired[BlockchainInstantTypeDef],
    },
)

GetTokenBalanceInputRequestTypeDef = TypedDict(
    "GetTokenBalanceInputRequestTypeDef",
    {
        "tokenIdentifier": TokenIdentifierTypeDef,
        "ownerIdentifier": OwnerIdentifierTypeDef,
        "atBlockchainInstant": NotRequired[BlockchainInstantTypeDef],
    },
)

GetTokenBalanceOutputTypeDef = TypedDict(
    "GetTokenBalanceOutputTypeDef",
    {
        "ownerIdentifier": OwnerIdentifierTypeDef,
        "tokenIdentifier": TokenIdentifierTypeDef,
        "balance": str,
        "atBlockchainInstant": BlockchainInstantTypeDef,
        "lastUpdatedTime": BlockchainInstantTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTransactionsInputRequestTypeDef = TypedDict(
    "ListTransactionsInputRequestTypeDef",
    {
        "address": str,
        "network": QueryNetworkType,
        "fromBlockchainInstant": NotRequired[BlockchainInstantTypeDef],
        "toBlockchainInstant": NotRequired[BlockchainInstantTypeDef],
        "sort": NotRequired[ListTransactionsSortTypeDef],
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)

TokenBalanceTypeDef = TypedDict(
    "TokenBalanceTypeDef",
    {
        "balance": str,
        "atBlockchainInstant": BlockchainInstantTypeDef,
        "ownerIdentifier": NotRequired[OwnerIdentifierTypeDef],
        "tokenIdentifier": NotRequired[TokenIdentifierTypeDef],
        "lastUpdatedTime": NotRequired[BlockchainInstantTypeDef],
    },
)

BatchGetTokenBalanceInputRequestTypeDef = TypedDict(
    "BatchGetTokenBalanceInputRequestTypeDef",
    {
        "getTokenBalanceInputs": NotRequired[Sequence[BatchGetTokenBalanceInputItemTypeDef]],
    },
)

BatchGetTokenBalanceOutputTypeDef = TypedDict(
    "BatchGetTokenBalanceOutputTypeDef",
    {
        "tokenBalances": List[BatchGetTokenBalanceOutputItemTypeDef],
        "errors": List[BatchGetTokenBalanceErrorItemTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListTokenBalancesOutputTypeDef = TypedDict(
    "ListTokenBalancesOutputTypeDef",
    {
        "tokenBalances": List[TokenBalanceTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
