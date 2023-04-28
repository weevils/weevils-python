from uuid import uuid4

from .._utils import is_uuid


def test_uuid_detection():
    assert not is_uuid("bananas")
    assert not is_uuid(None)
    assert is_uuid(uuid4())
    assert is_uuid("ed0c1396-f424-4047-8a55-3fd76654dd63")
