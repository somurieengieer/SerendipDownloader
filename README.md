SelendipDownloader
====

SelendipサイトのPDFファイルを一括ダウンロードするためのプログラム。
ワーキングスペースにbooksディレクトリを作成し、PDFファイルを保存する。

# Description
SelendipサイトからPDFファイルを保存するには１つ１つ書籍ページを開き、書籍PDFをダウンロードしなければならない。
当プログラムにより一括ダウンロードを実現する。  

# Usage
### 事前準備
- ChromeDriverをダウンロードし、パスを通す必要がある
https://catcherweb.com/selenium-chromedriver/  

### 実行
- SerendipDownloader.pyを実行する。
- メールアドレス（ID）、パスワードを入力する
- ブラウザが起動し、自動でファイルの一覧を取得・ダウンロードを行う

### チューニング

アクセス制限等があるため以下の設定値は適当な値を設定する。SerendipDownloader.pyの上部に定数設定箇所あり。
- アクセスエラー時のリトライ回数
- アクセスエラー時の待ち秒数
- ファイル保存先ディレクトリ
