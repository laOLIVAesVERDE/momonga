# 記事本文スクレイパー

NHK「みんなでプラス」の記事本文（タイトル、日付、URL、本文）を取得するスクレイパーです。

## 使い方

### 前提条件

まず、親ディレクトリで仮想環境をセットアップしてください：

```bash
cd ..
./setup.sh
```

### 単一記事の取得

```bash
# 基本的な実行
./run_article.sh "https://www.nhk.or.jp/minplus/0026/topic054.html"

# 整形されたJSON出力
./run_article.sh "https://www.nhk.or.jp/minplus/0026/topic054.html" --pretty

# 出力ファイル名を指定
./run_article.sh "https://www.nhk.or.jp/minplus/0026/topic054.html" -o article_054.json --pretty
```

### 複数記事の一括取得

```bash
# デフォルト（カテゴリ0026、001-300を一括取得、output/0026/に保存）
./run_batch.sh

# 範囲を指定して取得（例: 001-050）
./run_batch.sh --start 1 --end 50

# カテゴリIDを指定
./run_batch.sh --start 1 --end 100 --category 0014  # カテゴリ14 → output/0014/
./run_batch.sh --start 1 --end 100 --category 0011  # カテゴリ11 → output/0011/
./run_batch.sh --start 1 --end 100 --category 0006  # カテゴリ6 → output/0006/

# 複数カテゴリを順次取得
./run_batch.sh --start 1 --end 300 --category 0026
./run_batch.sh --start 1 --end 300 --category 0014
./run_batch.sh --start 1 --end 300 --category 0011
./run_batch.sh --start 1 --end 300 --category 0006
```

**カテゴリについて:**
- **0026** - 性暴力を考える
- **0014** - 新型コロナ関連
- **0011** - その他のテーマ
- **0006** - その他のテーマ

**注意事項:**
- ページが存在しない場合は自動的にスキップします
- サーバー負荷軽減のため、各記事の取得後に1秒待機します
- 大量取得（300件）の場合、完了まで時間がかかります
- カテゴリIDは4桁形式で指定してください（例: 0026, 0014）
- 出力は `output/{category}/` にカテゴリごとに分けて保存されます

## 出力形式

```json
{
    "title": "記事タイトル",
    "date": "YYYY年M月D日",
    "url": "記事URL",
    "content": "記事本文（長文）"
}
```

## ファイル構成

- `article_scraper.py` - メインスクリプト
- `run_article.sh` - 単一記事取得用シェルスクリプト
- `batch_scraper.py` - 一括取得スクリプト
- `run_batch.sh` - 一括取得実行用シェルスクリプト
- `output/` - 一括取得時のデフォルト出力ディレクトリ
