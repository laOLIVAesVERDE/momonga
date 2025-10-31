#!/bin/bash
# NHK コメントスクレイパー実行スクリプト

# 仮想環境の確認
if [ ! -d "../venv" ]; then
    echo "❌ 仮想環境が見つかりません。"
    echo "親ディレクトリで ../setup.sh を実行してください。"
    exit 1
fi

# 仮想環境を有効化
source ../venv/bin/activate

# 引数をチェック
if [ $# -eq 0 ]; then
    echo "使い方: ./run.sh <URL> [オプション]"
    echo ""
    echo "例:"
    echo "  ./run.sh \"https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html\""
    echo "  ./run.sh \"https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html\" --pretty"
    echo "  ./run.sh \"https://www.nhk.or.jp/minplus/0026/comments/0026_054/index.html\" -o output.json --pretty"
    echo ""
    echo "ヘルプ:"
    echo "  ./run.sh --help"
    deactivate
    exit 1
fi

# スクレイパーを実行
python nhk_comment_scraper.py "$@"

# 仮想環境を無効化
deactivate
