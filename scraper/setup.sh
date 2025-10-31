#!/bin/bash
# 仮想環境のセットアップスクリプト

echo "仮想環境を作成中..."
python3 -m venv venv

echo "仮想環境を有効化中..."
source venv/bin/activate

echo "必要なパッケージをインストール中..."
pip install -r requirements.txt

echo ""
echo "✅ セットアップ完了！"
echo ""
echo "次回以降は以下のコマンドで仮想環境を有効化してください："
echo "  source venv/bin/activate"
echo ""
echo "スクレイパーの実行："
echo "  python nhk_comment_scraper.py \"URL\""
echo ""
echo "仮想環境を終了する場合："
echo "  deactivate"

