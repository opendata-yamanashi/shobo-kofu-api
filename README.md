# 消防水利施設一覧（消火栓） API
消防水利施設一覧（消火栓）

## 出典:
* [消防水利施設一覧（消火栓)](https://www.city.kofu.yamanashi.jp/joho/opendata/shisetsu/index.html)

## API 仕様
(後で書く)

## ライセンス
本ソフトウェアは、[MITライセンス](https://github.com/opendata-yamanashi/onsen-api/blob/main/LICENSE.txt)の元提供されています。

## Installation

* how to setup  
```
$ git clone https://github.com/opendata-yamanashi/shobo-kofu-api
$ pip install -r requirements.txt
```
* access my application!
```
$ uvicorn app.main:app --reload 
$ curl http://localhost:8000/
```

## Environment variables
環境変数を設定する場合は、.envファイルを作成し、記載してください。
.envファイルが無くても開発環境で動作するようになっています。

- ### PYTHON_ENV
  実行環境を指定する文字列です。開発環境ではdevelopment, 本番環境ではproductionを設定してください。デフォルトはdevelopmentです。  

- ### PORT
  サーバーを公開するポートを指定する数値です。デフォルトは8000です。

done
