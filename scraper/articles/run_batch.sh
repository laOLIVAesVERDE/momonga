#!/bin/bash
# NHK 記事本文一括スクレイパー実行スクリプト

# 仮想環境の確認
if [ ! -d "../venv" ]; then
    echo "❌ 仮想環境が見つかりません。"
    echo "親ディレクトリで ../setup.sh を実行してください。"
    exit 1
fi

# 仮想環境を有効化
source ../venv/bin/activate

# 引数がない場合はデフォルト（1-300）で実行
if [ $# -eq 0 ]; then
    echo "デフォルト設定で実行します（記事ID: 001-300）"
    python batch_scraper.py --start 1 --end 300
else
    # 引数をそのまま渡す
    python batch_scraper.py "$@"
fi

# 仮想環境を無効化
deactivate

