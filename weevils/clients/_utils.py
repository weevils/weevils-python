from uuid import UUID


def is_uuid(val: str) -> bool:
    if val is None:
        return False
    if not isinstance(val, UUID):
        try:
            UUID(val)
        except ValueError:
            return False
    return True
