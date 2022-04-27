from pydantic import BaseModel, Field

class ShoboData(BaseModel):
    code: str = Field(None, alias="コード名称(地区コード)")
    town: str = Field(None, alias="町名(漢字)")
    lat: int = Field(None, alias="座標X(日本測地系)")
    lon: int = Field(None, alias="座標Y(日本測地系)")
