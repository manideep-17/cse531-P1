from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class QueryRequest(_message.Message):
    __slots__ = ["id", "event_id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ...) -> None: ...

class QueryResponse(_message.Message):
    __slots__ = ["id", "event_id", "balance"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    balance: int
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., balance: _Optional[int] = ...) -> None: ...

class DepositRequest(_message.Message):
    __slots__ = ["id", "event_id", "money"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    money: int
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., money: _Optional[int] = ...) -> None: ...

class DepositResponse(_message.Message):
    __slots__ = ["id", "event_id", "result"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    result: str
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., result: _Optional[str] = ...) -> None: ...

class WithdrawRequest(_message.Message):
    __slots__ = ["id", "event_id", "money"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    MONEY_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    money: int
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., money: _Optional[int] = ...) -> None: ...

class WithdrawResponse(_message.Message):
    __slots__ = ["id", "event_id", "result"]
    ID_FIELD_NUMBER: _ClassVar[int]
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    id: int
    event_id: int
    result: str
    def __init__(self, id: _Optional[int] = ..., event_id: _Optional[int] = ..., result: _Optional[str] = ...) -> None: ...

class PropagateDepositRequest(_message.Message):
    __slots__ = ["balance"]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    balance: int
    def __init__(self, balance: _Optional[int] = ...) -> None: ...

class PropagateDepositResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...

class PropagateWithdrawRequest(_message.Message):
    __slots__ = ["balance"]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    balance: int
    def __init__(self, balance: _Optional[int] = ...) -> None: ...

class PropagateWithdrawResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: str
    def __init__(self, result: _Optional[str] = ...) -> None: ...
