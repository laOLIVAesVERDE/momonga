# コメントスクレイパー

NHK「みんなでプラス」のコメントを取得するスクレイパーです。

## 使い方

### 前提条件

まず、親ディレクトリで仮想環境をセットアップしてください：

```bash
cd ..
./setup.sh
```

### 単一記事のコメント取得

```bash
# 基本的な実行
./run.sh "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html"

# 整形されたJSON出力
./run.sh "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html" --pretty

# 出力ファイル名を指定
./run.sh "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html" -o output.json --pretty
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

### プログラムから使用する例

```bash
python example.py
```

## 出力形式

```json
[
  {
    "type": "感想|体験談|提言|質問|悩み",
    "name": "投稿者名",
    "age": "20代|30代..." または null,
    "gender": "男性|女性" または null,
    "date": "YYYY年M月D日",
    "content": "コメント本文"
  }
]
```

## ファイル構成

- `nhk_comment_scraper.py` - コメントスクレイパーのメインクラス
- `run.sh` - 単一記事のコメント取得スクリプト
- `batch_scraper.py` - 一括取得スクリプト
- `run_batch.sh` - 一括取得実行スクリプト
- `example.py` - プログラムから使用する例
- `output/` - 一括取得時のデフォルト出力ディレクトリ
