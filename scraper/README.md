# NHK みんなでプラス スクレイパー

NHKの「みんなでプラス」サイトの記事本文とコメントを取得し、JSON形式で保存するスクレイピングツールです。

## ディレクトリ構成

```
scraper/
├── articles/                 # 記事本文スクレイパー
│   ├── article_scraper.py
│   ├── run_article.sh
│   ├── batch_scraper.py
│   ├── run_batch.sh
│   ├── output/              # 一括取得時の出力先
│   │   ├── 0026/           # カテゴリ26の記事本文
│   │   ├── 0014/           # カテゴリ14の記事本文
│   │   ├── 0011/           # カテゴリ11の記事本文
│   │   └── 0006/           # カテゴリ6の記事本文
│   └── README.md
├── comments_scraper/         # コメントスクレイパー
│   ├── nhk_comment_scraper.py
│   ├── run.sh
│   ├── batch_scraper.py
│   ├── run_batch.sh
│   ├── example.py
│   ├── output/              # 一括取得時の出力先
│   │   ├── 0026/           # カテゴリ26のコメント
│   │   ├── 0014/           # カテゴリ14のコメント
│   │   ├── 0011/           # カテゴリ11のコメント
│   │   └── 0006/           # カテゴリ6のコメント
│   └── README.md
├── venv/                    # 仮想環境
├── merge_articles.py        # 記事とコメントのマージスクリプト
├── merge.sh                 # マージ実行スクリプト
├── scrape_all_categories.sh # 全カテゴリ一括取得スクリプト
├── setup.sh                 # セットアップスクリプト
├── requirements.txt         # 依存パッケージ
└── README.md                # このファイル

プロジェクトルート/articles/ （マージ後の最終出力先）
├── 0026/                    # カテゴリ26（性暴力を考える）
│   ├── article_001.json    # 記事本文 + コメント
│   ├── article_002.json
│   └── ...
├── 0014/                    # カテゴリ14（新型コロナ）
├── 0011/                    # カテゴリ11
└── 0006/                    # カテゴリ6
```

## 機能

### 記事本文スクレイパー（articles/）
- 記事のタイトル、日付、URL、本文を取得
- 複数記事の一括取得機能

### コメントスクレイパー（comments_scraper/）
- 指定されたURLからコメントを自動取得
- ページネーション対応（複数ページのコメントを一括取得）
- 複数記事の一括取得機能
- 以下の情報を抽出してJSON形式で保存：
  - `type`: コメントタイプ（感想、体験談、悩みなど）
  - `name`: 投稿者名
  - `age`: 年齢（nullable）
  - `gender`: 性別（nullable）
  - `date`: 投稿日
  - `content`: コメント本文

### マージ機能
- 記事本文とコメントを連結してプロジェクトルートの`articles/{category}/`に保存
- カテゴリごとにフォルダを分けて整理
- コメントがない場合は空の配列を設定

## インストール

### 方法1: 自動セットアップ（推奨）

```bash
cd scraper
chmod +x setup.sh
./setup.sh
```

このスクリプトが自動的に：
1. 仮想環境（venv）を作成
2. 必要なパッケージをインストール

### 方法2: 手動セットアップ

```bash
cd scraper

# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate

# パッケージをインストール
pip install -r requirements.txt
```

### 次回以降の使用

スクレイパーを使う前に、必ず仮想環境を有効化してください：

```bash
cd scraper
source venv/bin/activate
```

終了する場合：

```bash
deactivate
```

## クイックスタート

全カテゴリのデータを一括で取得する場合：

```bash
cd scraper

# 1. セットアップ（初回のみ）
./setup.sh

# 2. 全カテゴリ一括取得（記事 + コメント + マージ）
./scrape_all_categories.sh
```

完了すると、プロジェクトルートの `articles/` フォルダに、カテゴリごとに分けて全記事とコメントが保存されます：

```
articles/
├── 0026/           # 性暴力を考える
│   ├── article_001.json
│   ├── article_002.json
│   └── ...
├── 0014/           # 新型コロナ関連
│   ├── article_001.json
│   └── ...
├── 0011/           # その他のテーマ
└── 0006/           # その他のテーマ
```

## カテゴリについて

NHKみんなでプラスには以下のカテゴリがあります：

- **0026** - 性暴力を考える
- **0014** - 新型コロナ関連
- **0011** - その他のテーマ
- **0006** - その他のテーマ

各カテゴリごとに記事とコメントが分けて保存されます。

## 全体の流れ

1. **記事本文の取得** - `articles/` で記事本文を取得（カテゴリごとに `output/{category}/` に保存）
2. **コメントの取得** - `comments_scraper/` でコメントを取得（カテゴリごとに `output/{category}/` に保存）
3. **マージ** - `merge.sh` で記事本文とコメントを連結してプロジェクトルートの `articles/{category}/` に保存

**ディレクトリ構造:**
```
articles/
├── 0026/           # カテゴリ26の記事データ（記事本文 + コメント）
│   ├── article_001.json
│   ├── article_002.json
│   └── ...
├── 0014/           # カテゴリ14の記事データ
├── 0011/           # カテゴリ11の記事データ
└── 0006/           # カテゴリ6の記事データ
```

## 使い方

### 📰 方法1: 記事本文のスクレイピング

#### 単一記事の取得

```bash
cd scraper/articles

# 基本的な使い方
./run_article.sh "https://www.nhk.or.jp/minplus/0026/topic054.html"

# 整形されたJSON出力
./run_article.sh "https://www.nhk.or.jp/minplus/0026/topic054.html" --pretty

# 出力ファイル名を指定
./run_article.sh "https://www.nhk.or.jp/minplus/0026/topic054.html" -o article_054.json --pretty
```

#### 複数記事の一括取得

```bash
cd scraper/articles

# デフォルト（カテゴリ0026、001-300を一括取得、output/0026/に保存）
./run_batch.sh

# 範囲を指定して取得（例: 001-050）
./run_batch.sh --start 1 --end 50

# カテゴリIDを指定
./run_batch.sh --start 1 --end 100 --category 0014  # カテゴリ14
./run_batch.sh --start 1 --end 100 --category 0011  # カテゴリ11
./run_batch.sh --start 1 --end 100 --category 0006  # カテゴリ6

# 複数カテゴリを順次取得
./run_batch.sh --start 1 --end 300 --category 0026  # output/0026/
./run_batch.sh --start 1 --end 300 --category 0014  # output/0014/
./run_batch.sh --start 1 --end 300 --category 0011  # output/0011/
./run_batch.sh --start 1 --end 300 --category 0006  # output/0006/
```

**注意:** カテゴリIDは4桁形式で指定してください（例: 0026, 0014, 0011, 0006）

詳細は [articles/README.md](articles/README.md) を参照してください。

**出力形式:**
```json
{
    "title": "記事タイトル",
    "date": "YYYY年M月D日",
    "url": "記事URL",
    "content": "記事本文（長文）"
}
```

### 💬 方法2: コメントのスクレイピング

#### 単一記事のコメント取得

```bash
cd scraper/comments_scraper

# 基本的な使い方
./run.sh "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html"

# 整形されたJSON出力
./run.sh "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html" --pretty

# 出力ファイル名を指定
./run.sh "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html" -o output.json --pretty
```

#### 複数記事の一括取得

```bash
cd scraper/comments_scraper

# デフォルト（カテゴリ0026、001-300を一括取得、output/0026/に保存）
./run_batch.sh

# 範囲を指定して取得（例: 001-050）
./run_batch.sh --start 1 --end 50

# カテゴリIDを指定
./run_batch.sh --start 1 --end 100 --category 0014  # カテゴリ14
./run_batch.sh --start 1 --end 100 --category 0011  # カテゴリ11
./run_batch.sh --start 1 --end 100 --category 0006  # カテゴリ6

# 複数カテゴリを順次取得
./run_batch.sh --start 1 --end 300 --category 0026  # output/0026/
./run_batch.sh --start 1 --end 300 --category 0014  # output/0014/
./run_batch.sh --start 1 --end 300 --category 0011  # output/0011/
./run_batch.sh --start 1 --end 300 --category 0006  # output/0006/
```

**注意:** カテゴリIDは4桁形式で指定してください（例: 0026, 0014, 0011, 0006）

詳細は [comments_scraper/README.md](comments_scraper/README.md) を参照してください。

**注意事項:**
- ページが存在しない場合は自動的にスキップします
- サーバー負荷軽減のため、各記事の取得後に1秒待機します
- 大量取得（300件）の場合、完了まで時間がかかります

### 方法3: 記事本文とコメントのマージ

記事本文（`articles/output/{category}/`）とコメント（`comments_scraper/output/{category}/`）を連結して、プロジェクトルートの`articles/{category}/`フォルダに保存します：

```bash
cd scraper

# デフォルト（カテゴリ0026） → ../articles/0026/
./merge.sh

# カテゴリを指定してマージ
./merge.sh --category 0026  # 性暴力を考える → ../articles/0026/
./merge.sh --category 0014  # 新型コロナ関連 → ../articles/0014/
./merge.sh --category 0011  # その他のテーマ → ../articles/0011/
./merge.sh --category 0006  # その他のテーマ → ../articles/0006/

# カスタムディレクトリを指定
./merge.sh --articles-dir articles/output --comments-dir comments_scraper/output --output-dir ../articles --category 0026
```

**出力先:**
- カテゴリ0026 → `/articles/0026/article_001.json`
- カテゴリ0014 → `/articles/0014/article_001.json`
- カテゴリ0011 → `/articles/0011/article_001.json`
- カテゴリ0006 → `/articles/0006/article_001.json`

**出力形式:**
```json
{
    "title": "記事タイトル",
    "date": "YYYY年M月D日",
    "url": "記事URL",
    "content": "記事本文",
    "comments": [
        {
            "type": "感想",
            "name": "投稿者名",
            "age": "20代",
            "gender": "男性",
            "date": "YYYY年M月D日",
            "content": "コメント本文"
        }
    ]
}
```

**注意:**
- コメントがない場合は `comments: []` として空配列が設定されます
- マージ前に記事本文とコメントを取得しておく必要があります
- 各カテゴリごとにフォルダ分けされます

### 🚀 方法4: 全カテゴリ一括取得（推奨）

全カテゴリ（0026, 0014, 0011, 0006）の記事とコメントを自動で取得してマージします：

```bash
cd scraper

# 全カテゴリを一括処理（記事取得 → コメント取得 → マージ）
./scrape_all_categories.sh
```

このスクリプトは以下を自動実行します：
1. 各カテゴリの記事本文を取得（001-300） → `articles/output/{category}/`
2. 各カテゴリのコメントを取得（001-300） → `comments_scraper/output/{category}/`
3. 記事本文とコメントをマージして `../articles/{category}/` にカテゴリごとに保存

**最終的な出力:**
```
articles/
├── 0026/article_001.json, article_002.json, ...
├── 0014/article_001.json, article_002.json, ...
├── 0011/article_001.json, article_002.json, ...
└── 0006/article_001.json, article_002.json, ...
```

**注意:** 全カテゴリ・全記事の取得には相当な時間がかかります

### 方法5: 手動で仮想環境を管理

#### 記事スクレイパー

```bash
cd scraper
source venv/bin/activate
cd articles

python article_scraper.py "https://www.nhk.or.jp/minplus/0026/topic054.html" --pretty -o article_054.json

deactivate
```

#### コメントスクレイパー

```bash
cd scraper
source venv/bin/activate
cd comments_scraper

# 単一記事
python nhk_comment_scraper.py "https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html" --pretty

# 一括取得
python batch_scraper.py --start 1 --end 50

# プログラムから呼び出す例
python example.py

deactivate
```

## 出力例

```json
[
  {
    "type": "感想",
    "name": "キジトラ",
    "age": "20代",
    "gender": "男性",
    "date": "2025年2月27日",
    "content": "性行為は心と命に関わります。暴行や不倫、痴漢といった行為に発展すれば..."
  },
  {
    "type": "体験談",
    "name": "はなえつ",
    "age": "50代",
    "gender": "女性",
    "date": "2025年2月21日",
    "content": "現役自衛官に強姦未遂に遭いました..."
  }
]
```

## 注意事項

- このツールは教育・研究目的で作成されています
- スクレイピングを実行する際は、対象サイトの利用規約を確認してください
- 過度なアクセスはサーバーに負荷をかけるため、適切な間隔を空けて実行してください
- 取得したデータの取り扱いには十分注意してください

## ライセンス

MIT License
