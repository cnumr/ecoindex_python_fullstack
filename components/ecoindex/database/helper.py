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
    if date_from:
        statement = statement.where(ApiEcoindex.date >= date_from)

    if date_to:
        statement = statement.where(ApiEcoindex.date <= date_to)

    return statement


def check_if_table_exists(conn, table_name) -> bool:
    inspector = Inspector.from_engine(conn)
    return table_name in inspector.get_table_names()


def check_if_column_exists(conn, table_name, column_name) -> bool:
    inspector = Inspector.from_engine(conn)
    return column_name in [c["name"] for c in inspector.get_columns(table_name)]
