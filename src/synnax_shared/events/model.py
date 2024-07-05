from typing import Generic, NotRequired, TypedDict, TypeVar

CategoryName = TypeVar("CategoryName", bound=str)
TypeName = TypeVar("TypeName", bound=str)
DataT = TypeVar("DataT")


class DomainEventSource(TypedDict):
    service: str
    sessionId: NotRequired[str]
    userId: NotRequired[str]
    systemId: NotRequired[str]
    organizationId: NotRequired[str]
    apiKeyId: NotRequired[str]


class DomainEvent(TypedDict, Generic[CategoryName, TypeName, DataT]):
    category: CategoryName
    type: TypeName
    itemId: str
    sequence: int
    data: DataT
    createdAt: str
    persistedAt: str
    source: DomainEventSource
