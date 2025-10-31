#!/bin/bash
# NHK 記事本文スクレイパー実行スクリプト

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
    echo "使い方: ./run_article.sh <URL> [オプション]"
    echo ""
    echo "例:"
    echo "  ./run_article.sh \"https://www.nhk.or.jp/minplus/0026/topic054.html\""
    echo "  ./run_article.sh \"https://www.nhk.or.jp/minplus/0026/topic054.html\" --pretty"
    echo "  ./run_article.sh \"https://www.nhk.or.jp/minplus/0026/topic054.html\" -o article_054.json --pretty"
    echo ""
    echo "ヘルプ:"
    echo "  ./run_article.sh --help"
    deactivate
    exit 1
fi

# スクレイパーを実行
python article_scraper.py "$@"

# 仮想環境を無効化
deactivate
