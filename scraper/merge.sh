#!/bin/bash
# 記事本文とコメントをマージするスクリプト

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "❌ 仮想環境が見つかりません。"
    echo "まず ./setup.sh を実行してください。"
    exit 1
fi

# 仮想環境を有効化
source venv/bin/activate

# マージスクリプトを実行
python merge_articles.py "$@"

# 仮想環境を無効化
deactivate

