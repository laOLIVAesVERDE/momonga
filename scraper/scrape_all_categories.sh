#!/bin/bash
# 全カテゴリの記事とコメントを一括で取得してマージするスクリプト

# 仮想環境の確認
if [ ! -d "venv" ]; then
    echo "❌ 仮想環境が見つかりません。"
    echo "まず ./setup.sh を実行してください。"
    exit 1
fi

# カテゴリリスト
CATEGORIES=("0026" "0014" "0011" "0006")

echo "============================================================"
echo "全カテゴリの一括取得を開始します"
echo "カテゴリ: ${CATEGORIES[@]}"
echo "============================================================"
echo ""

for category in "${CATEGORIES[@]}"; do
    echo ""
    echo "▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼"
    echo "カテゴリ $category の処理を開始"
    echo "▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼"
    echo ""
    
    # 1. 記事本文を取得
    echo "【ステップ1】記事本文の取得"
    cd articles
    ./run_batch.sh --start 1 --end 300 --category "$category"
    cd ..
    echo ""
    
    # 2. コメントを取得
    echo "【ステップ2】コメントの取得"
    cd comments_scraper
    ./run_batch.sh --start 1 --end 300 --category "$category"
    cd ..
    echo ""
    
    # 3. マージ
    echo "【ステップ3】マージ"
    ./merge.sh --category "$category"
    echo ""
    
    echo "✅ カテゴリ $category の処理が完了しました"
    echo ""
done

echo ""
echo "============================================================"
echo "🎉 全カテゴリの処理が完了しました！"
echo "============================================================"
echo "出力先: ../articles/"
echo ""
echo "取得したファイルを確認:"
echo "  ls -lh ../articles/article_*.json"
echo "============================================================"
