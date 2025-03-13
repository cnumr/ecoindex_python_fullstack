from datetime import date

from ecoindex.database.models import ApiEcoindex
from sqlalchemy.engine.reflection import Inspector
from sqlmodel.sql.expression import SelectOfScalar

SelectOfScalar.inherit_cache = True  # type: ignore


def date_filter(
    statement: SelectOfScalar,
    date_from: date | None = None,
    date_to: date | None = None,
) -> SelectOfScalar:
    if date_from and ApiEcoindex.date:
        statement = statement.where(ApiEcoindex.date >= date_from)

    if date_to and ApiEcoindex.date:
        statement = statement.where(ApiEcoindex.date <= date_to)

    return statement


def table_exists(conn, table_name) -> bool:
    inspector = Inspector.from_engine(conn)
    return table_name in inspector.get_table_names()


def column_exists(conn, table_name, column_name) -> bool:
    inspector = Inspector.from_engine(conn)
    return column_name in [c["name"] for c in inspector.get_columns(table_name)]


def index_exists(conn, table_name, index_name) -> bool:
    inspector = Inspector.from_engine(conn)
    return index_name in [i["name"] for i in inspector.get_indexes(table_name)]
