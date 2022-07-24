from typing import Any, Dict, List, Sequence, Union, cast

from pathlib import Path
import csv
from io import BytesIO

import pandas as pd
from pandas import DataFrame
import requests
import neologdn

from model import ShoboData


class FetcherBase():
    def __init__(self, url: str, sheet_name: Union[str, Path], *, sheet_header: Union[int, Sequence[int], None] = 0) -> None:
        self.url = url
        self.sheet_name = sheet_name
        self.sheet_header = sheet_header

    def fetch(self):
        res = requests.get(self.url, allow_redirects=True)
        file: Any = BytesIO(res.content)
        df = pd.read_excel(
            file,
            sheet_name=str(self.sheet_name),
            header=self.sheet_header
        ).dropna()

        df = self.parse(df)

        return df.to_dict("records")

    def reflect(self, records: List[Dict[str, Any]]) -> None:
        pass

    def parse(self, df: DataFrame) -> DataFrame:
        return df


class Fetcher(FetcherBase):
    def parse(self, df: DataFrame) -> DataFrame:
        df.columns = [neologdn.normalize(i) for i in df.columns]
        df["コード名称(地区コード)"] = df["コード名称(地区コード)"].map(neologdn.normalize)
        df["町名(漢字)"] = df["町名(漢字)"].map(neologdn.normalize)

        return df

    def reflect(self, records: List[Dict[str, Any]], dir: Path, name: str):
        if not dir.exists():
            dir.mkdir()

        schema = ShoboData.schema().get("properties")
        keys = cast(dict, schema).keys()

        with open((dir / name).with_suffix(".csv"), "w") as f:
            writer = csv.DictWriter(f, keys, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(records)


if __name__ == "__main__":
    FILE_URL = "https://www.city.kofu.yamanashi.jp/joho/opendata/shisetsu/documents/syokasenspot_20200401.xlsx"
    SHEET_NAME = "消防水利施設一覧（消火栓）※20200401現在"

    FILE_DIR = Path(__file__).absolute().parent.parent / "data"
    FILE_NAME = FILE_URL.split("/")[-1]

    fetcher = Fetcher(FILE_URL, SHEET_NAME)
    records = fetcher.fetch()
    fetcher.reflect(records, FILE_DIR, FILE_NAME)
