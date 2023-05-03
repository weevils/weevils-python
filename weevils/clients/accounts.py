from typing import List
from uuid import UUID

from ..client_base import ClientBase
from ..dtos import Account


class AccountsClient(ClientBase):
    DTO_CLASS = Account

    def get(self, account_id: UUID) -> Account:
        return self._get(f"/account/{account_id}")

    def list(self, offset: int = 0, limit: int = 100) -> List[Account]:
        query = {"limit": limit, "offset": offset}
        return self._list("/account/", query)
