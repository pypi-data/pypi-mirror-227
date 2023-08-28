class Default:

    def __init__(self, *args, **kwargs) -> None:
        pass


try:
    from pydantic import (
        BaseModel as PydanticBaseModel,
        Field as PydanticField
    )
except Exception:
    PydanticBaseModel = Default
    PydanticField = Default


try:
    from sqlalchemy.orm.decl_api import (
        DeclarativeMeta as SQLAlchemyDeclarativeMeta,
        declarative_base as SQLAlchemyDeclarativeBase
    )
    from sqlalchemy import (
        Column as SQLAlchemyColumn,
        Integer as SQLAlchemyInteger,
        String as SQLAlchemyString
    )
except Exception:
    SQLAlchemyDeclarativeMeta = Default
    SQLAlchemyDeclarativeBase = Default
    SQLAlchemyColumn = Default
    SQLAlchemyInteger = Default
    SQLAlchemyString = Default
