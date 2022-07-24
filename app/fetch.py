from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Sequence, Union

from pathlib import Path
import io

import pandas as pd
import requests
import neologdn

from db import ShoboDataWithId, get_session


class AbstractFetcher(metaclass=ABCMeta):
    def __init__(self, url: str, sheet_name: Union[str, Path], *, sheet_header: Union[int, Sequence[int], None] = 0) -> None:
        self.url = url
        self.sheet_name = sheet_name
        self.sheet_header = sheet_header

    def fetch(self):
        records = self.download()
        self.reflect(records)

    def download(self):
        res = requests.get(self.url, allow_redirects=True)
        file: Any = io.BytesIO(res.content)
        df = pd.read_excel(
            file,
            sheet_name=str(self.sheet_name),
            header=self.sheet_header
        ).dropna()

        df = self.parse(df)

        return df.to_dict("records")

    @abstractmethod
    def parse(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    @abstractmethod
    def reflect(self, records: List[Dict[str, Any]]) -> None:
        pass


class Fetcher(AbstractFetcher):
    def parse(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [neologdn.normalize(i) for i in df.columns]
        df["コード名称(地区コード)"] = df["コード名称(地区コード)"].map(neologdn.normalize)
        df["町名(漢字)"] = df["町名(漢字)"].map(neologdn.normalize)

        return df

    def reflect(self, records: List[Dict[str, Any]]):
        with get_session() as session:
            for record in records:
                session.add(ShoboDataWithId(**record))
            session.commit()


if __name__ == "__main__":
    FILE_URL = "https://www.city.kofu.yamanashi.jp/joho/opendata/shisetsu/documents/syokasenspot_20200401.xlsx"
    SHEET_NAME = "消防水利施設一覧（消火栓）※20200401現在"

    Fetcher(FILE_URL, SHEET_NAME).fetch()
