from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, inspect


class ShoboData(SQLModel, allow_population_by_field_name=True):
    code: str = Field(None, alias="コード名称(地区コード)")
    town: str = Field(None, alias="町名(漢字)")
    lat: int = Field(None, alias="座標X(日本測地系)")
    lon: int = Field(None, alias="座標Y(日本測地系)")


class ShoboDataWithId(ShoboData, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


engine_url = "postgresql://postgres:password@db:5432/postgres"
engine = create_engine(engine_url)


def get_session():
    return Session(engine)


if __name__ == "__main__":
    if len(inspect(engine).get_table_names()) == 0:
        SQLModel.metadata.create_all(engine)
