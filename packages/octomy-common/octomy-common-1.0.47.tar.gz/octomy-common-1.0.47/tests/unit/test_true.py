import pprint
import logging
import os
import pytest

from fk.db.DatabaseConnection import DatabaseConnection
from fk.db.DatabaseConnectionAsync import DatabaseConnectionAsync


logger = logging.getLogger(__name__)

# fmt: off
dummy_config= {
    "db-hostname":"hello.com"
    ,"db-port":"1234"
    ,"db-username":"arnold"
    ,"db-password":"secret123"
    ,"db-database":"mydb"
}
# fmt: on


def test_true():
    logger.info("Dummy unit test")
    return True


def _test_db_get_same_twice():
    db1 = DatabaseConnection.get_connection(dummy_config)
    db2 = DatabaseConnection.get_connection(dummy_config)
    assert db1 == db2


def test_sync():
    db = DatabaseConnection(dummy_config)
    db._prepare_db()


@pytest.mark.asyncio
async def _test_async():
    db = DatabaseConnectionAsync(dummy_config)
    await db._prepare_db()
