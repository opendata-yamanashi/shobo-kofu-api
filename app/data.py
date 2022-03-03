from pathlib import Path
from download import Download
FILEURL = "https://www.city.kofu.yamanashi.jp/joho/opendata/shisetsu/documents/syokasenspot_20200401.xlsx"
import pandas as pd
import neologdn
from datetime import datetime

class Kofu_shobo():
    BASE_DIR = Path(__file__).absolute().parent.parent
    DATA_DIR = BASE_DIR / "data"

    def __init__(self):
        if not self.DATA_DIR.exists():
            self.DATA_DIR.mkdir()
        
        d = Download(FILEURL, self.DATA_DIR)
        d.download()
        self.fname = self.DATA_DIR / d.name
        self.version = datetime.now().strftime("%Y%m%d")
    
    def create_df(self):
        df = pd.read_excel(self.fname,sheet_name="消防水利施設一覧（消火栓）※20200401現在", header=0,usecols="B:E")
        df = df.dropna()
        df.columns = [neologdn.normalize(i) for i in df.columns]
        df["コード名称(地区コード)"] = df["コード名称(地区コード)"].map(neologdn.normalize)
        df["町名(漢字)"] = df["町名(漢字)"].map(neologdn.normalize)
        self.df = df

    def get_version(self):
        return self.version

    def query(self, keywords):
        return self.df.loc[self.df["コード名称(地区コード)"].str.contains(keywords) | self.df["町名(漢字)"].str.contains(keywords)]


if __name__ == "__main__":
    kf = Kofu_shobo()
    df = kf.create_df()
    